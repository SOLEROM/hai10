#!/usr/bin/env python3
"""
fixed_tracking_sender.py - Fixed pose detection with working SEI injection
Properly injects frame number and object count via SEI with debug output
Usage: python fixed_tracking_sender.py --device /dev/video0 --host 127.0.0.1 --port 5000
"""

import argparse
import sys
import time
import json
import threading
import queue

import gi
gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
from gi.repository import Gst, GstApp, GLib

# Optional Hailo Python helpers
try:
    import hailo
    HAVE_HAILO = True
except Exception:
    HAVE_HAILO = False

Gst.init(None)

class SEINALInjector:
    """Helper class for creating SEI NAL units with simple tracking metadata"""
    
    CUSTOM_UUID = b'SIMTRACK' + b'\x00' * 8  # Custom UUID for simple tracking data
    
    @staticmethod
    def create_sei_nal_unit(frame_num, object_count):
        """Create a SEI NAL unit with simple frame and object count data"""
        simple_data = {
            "frame": frame_num,
            "objects": object_count,
            "timestamp": time.time()
        }
        
        json_bytes = json.dumps(simple_data, separators=(',', ':')).encode('utf-8')
        payload_size = 16 + len(json_bytes)
        
        sei_payload = bytearray()
        sei_payload.append(0x05)  # user_data_unregistered
        
        # Encode payload size
        if payload_size < 255:
            sei_payload.append(payload_size)
        else:
            size_remaining = payload_size
            while size_remaining >= 255:
                sei_payload.append(0xFF)
                size_remaining -= 255
            sei_payload.append(size_remaining)
        
        sei_payload.extend(SEINALInjector.CUSTOM_UUID)
        sei_payload.extend(json_bytes)
        sei_payload.append(0x80)  # RBSP stop bit
        
        return b'\x00\x00\x00\x01\x06' + bytes(sei_payload)

class FixedTrackingSender:
    def __init__(self, device, hef, post_so, host, port, width=640, height=480):
        self.device = device
        self.hef = hef
        self.post_so = post_so
        self.host = host
        self.port = port
        self.width = width
        self.height = height
        
        # Simple tracking data
        self.frame_counter = 0
        self.current_object_count = 0
        self.sei_injection_counter = 0
        
        # SEI injection queue
        self.sei_queue = queue.Queue(maxsize=10)
        
        # Pipelines
        self.detection_pipeline = None
        self.transmission_pipeline = None
        self.appsrc = None
        
        # Threading
        self.running = False
        self.lock = threading.Lock()
        
    def create_detection_pipeline(self):
        """Create Hailo detection pipeline"""
        pipeline_str = f"""
        v4l2src device={self.device} name=source !
        video/x-raw,format=UYVY,width={self.width},height={self.height},framerate=30/1 !
        videorate drop-only=true !
        video/x-raw,framerate=8/1 !
        queue name=source_scale_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        videoscale name=source_videoscale n-threads=2 !
        queue name=source_convert_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        videoconvert n-threads=3 name=source_convert qos=false !
        video/x-raw,format=RGB,pixel-aspect-ratio=1/1 !
        tee name=t !
        
        queue name=inference_scale_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        videoscale name=inference_videoscale n-threads=2 qos=false !
        queue name=inference_convert_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        video/x-raw,pixel-aspect-ratio=1/1 !
        videoconvert name=inference_videoconvert n-threads=2 !
        queue name=inference_hailonet_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        hailonet name=inference_hailonet hef-path={self.hef} batch-size=1 force-writable=true !
        queue name=inference_hailofilter_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        hailofilter name=inference_hailofilter so-path={self.post_so} function-name=filter qos=false !
        queue name=inference_hailotracker_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        hailotracker name=hailo_tracker class-id=0 !
        identity name=tracking_callback signal-handoffs=true !
        fakesink
        
        t. !
        queue name=transmission_q leaky=no max-size-buffers=5 max-size-bytes=0 max-size-time=0 !
        videoconvert !
        videoscale !
        video/x-raw,format=I420,width=1280,height=720 !
        appsink name=frame_sink emit-signals=true sync=false max-buffers=5 drop=true
        """
        
        try:
            self.detection_pipeline = Gst.parse_launch(pipeline_str)
        except Exception as e:
            print(f"ERROR: Failed to create detection pipeline: {e}")
            sys.exit(1)
        
        # Connect tracking callback
        identity = self.detection_pipeline.get_by_name("tracking_callback")
        if identity:
            identity.connect("handoff", self.on_tracking_handoff)
        
        # Connect frame sink for transmission
        frame_sink = self.detection_pipeline.get_by_name("frame_sink")
        if frame_sink:
            frame_sink.connect("new-sample", self.on_frame_sample)
        
        # Bus handling
        bus = self.detection_pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_detection_message)
    
    def create_transmission_pipeline(self):
        """Create transmission pipeline with manual SEI injection"""
        # Create a custom pipeline that manually handles SEI injection
        pipeline_str = f"""
        appsrc name=src format=3 is-live=true caps=video/x-raw,format=I420,width=1280,height=720,framerate=8/1 !
        x264enc tune=zerolatency bitrate=2000 key-int-max=8 speed-preset=ultrafast bframes=0 !
        video/x-h264,stream-format=byte-stream !
        h264parse config-interval=1 !
        appsink name=h264_sink emit-signals=true sync=false max-buffers=10 drop=true
        """
        
        try:
            self.transmission_pipeline = Gst.parse_launch(pipeline_str)
        except Exception as e:
            print(f"ERROR: Failed to create transmission pipeline: {e}")
            sys.exit(1)
        
        # Get appsrc
        self.appsrc = self.transmission_pipeline.get_by_name("src")
        if self.appsrc:
            self.appsrc.set_property('format', Gst.Format.TIME)
            self.appsrc.set_property('is-live', True)
        
        # Connect H.264 sink
        h264_sink = self.transmission_pipeline.get_by_name("h264_sink")
        if h264_sink:
            h264_sink.connect("new-sample", self.on_h264_sample)
        
        # Create RTP transmission pipeline
        self.rtp_pipeline_str = f"""
        appsrc name=rtp_src format=3 is-live=true caps=video/x-h264,stream-format=byte-stream,alignment=au !
        rtph264pay config-interval=1 mtu=1400 pt=96 !
        application/x-rtp,media=video,encoding-name=H264,payload=96 !
        udpsink host={self.host} port={self.port} sync=false
        """
        
        try:
            self.rtp_pipeline = Gst.parse_launch(self.rtp_pipeline_str)
            self.rtp_appsrc = self.rtp_pipeline.get_by_name("rtp_src")
        except Exception as e:
            print(f"ERROR: Failed to create RTP pipeline: {e}")
            sys.exit(1)
        
        # Bus handling
        bus = self.transmission_pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_transmission_message)
        
        bus2 = self.rtp_pipeline.get_bus()
        bus2.add_signal_watch()
        bus2.connect("message", self.on_rtp_message)
    
    def on_tracking_handoff(self, identity, buffer):
        """Handle tracking data from Hailo pipeline"""
        self.frame_counter += 1
        object_count = 0
        
        if HAVE_HAILO:
            try:
                roi = hailo.get_roi_from_buffer(buffer)
                if roi is not None:
                    # Get objects
                    objs = []
                    try:
                        objs = list(roi.get_objects())
                    except Exception:
                        try:
                            objs = list(hailo.get_objects_from_roi(roi))
                        except Exception:
                            pass
                    
                    object_count = len(objs)
                    
                    if object_count > 0:
                        print(f"🎯 Frame {self.frame_counter}: {object_count} objects detected", flush=True)
                
            except Exception as e:
                print(f"[ERROR] Frame {self.frame_counter}: Hailo meta read failed: {e}", flush=True)
        
        # Store tracking data for SEI injection
        tracking_data = {
            'frame': self.frame_counter,
            'objects': object_count,
            'timestamp': time.time()
        }
        
        # Add to SEI queue (non-blocking)
        try:
            self.sei_queue.put_nowait(tracking_data)
        except queue.Full:
            # Remove oldest if queue is full
            try:
                self.sei_queue.get_nowait()
                self.sei_queue.put_nowait(tracking_data)
            except queue.Empty:
                pass
        
        print(f"📊 Tracking data queued: Frame {self.frame_counter}, Objects {object_count}", flush=True)
    
    def on_frame_sample(self, sink):
        """Handle video frames for transmission"""
        sample = sink.emit("pull-sample")
        if not sample or not self.appsrc:
            return Gst.FlowReturn.OK
        
        buffer = sample.get_buffer()
        
        # Push to H.264 encoding pipeline
        ret = self.appsrc.emit("push-buffer", buffer)
        return Gst.FlowReturn.OK
    
    def analyze_h264_frame(self, data):
        """Analyze H.264 frame structure for debugging"""
        nalus = []
        i = 0
        while i < len(data) - 4:
            if data[i:i+4] == b'\x00\x00\x00\x01':
                # Found start code
                nal_type = data[i+4] & 0x1F
                nalus.append(nal_type)
                i += 4
            else:
                i += 1
        return nalus
    
    def on_h264_sample(self, sink):
        """Handle H.264 encoded frames and inject SEI"""
        sample = sink.emit("pull-sample")
        if not sample or not self.rtp_appsrc:
            return Gst.FlowReturn.OK
        
        buffer = sample.get_buffer()
        
        # Get buffer data
        success, map_info = buffer.map(Gst.MapFlags.READ)
        if not success:
            return Gst.FlowReturn.OK
        
        data = bytes(map_info.data)
        buffer.unmap(map_info)
        
        # Analyze frame structure
        nalus = self.analyze_h264_frame(data)
        
        # Check if this is a keyframe (contains IDR - type 5)
        is_keyframe = 5 in nalus
        
        output_data = data
        
        print(f"🎬 H.264 frame: NALUs {nalus}, Keyframe: {is_keyframe}, Size: {len(data)} bytes", flush=True)
        
        # Inject SEI on keyframes if we have tracking data
        if is_keyframe:
            try:
                tracking_data = self.sei_queue.get_nowait()
                
                # Create SEI NAL unit
                frame_num = tracking_data['frame']
                obj_count = tracking_data['objects']
                
                sei_nal = SEINALInjector.create_sei_nal_unit(frame_num, obj_count)
                
                print(f"📝 Creating SEI: Frame {frame_num}, Objects {obj_count}", flush=True)
                print(f"📦 SEI NAL size: {len(sei_nal)} bytes, UUID: {SEINALInjector.CUSTOM_UUID[:8].hex()}", flush=True)
                
                # Find IDR frame position for insertion
                insert_pos = 0
                i = 0
                while i < len(data) - 4:
                    if data[i:i+4] == b'\x00\x00\x00\x01':
                        nal_type = data[i+4] & 0x1F
                        if nal_type == 5:  # IDR frame
                            insert_pos = i
                            break
                        i += 4
                    else:
                        i += 1
                
                # Insert SEI before IDR frame
                if insert_pos > 0:
                    output_data = data[:insert_pos] + sei_nal + data[insert_pos:]
                    print(f"💉 Inserted SEI at position {insert_pos} (before IDR)", flush=True)
                else:
                    # If no IDR found, insert at beginning
                    output_data = sei_nal + data
                    print(f"💉 Inserted SEI at beginning (no IDR found)", flush=True)
                
                self.sei_injection_counter += 1
                print(f"✅ SEI injection #{self.sei_injection_counter} successful! New size: {len(output_data)} bytes", flush=True)
                
                # Verify SEI was added
                new_nalus = self.analyze_h264_frame(output_data)
                print(f"🔍 After injection NALUs: {new_nalus}", flush=True)
                
            except queue.Empty:
                print("⚠️  Keyframe but no tracking data available for SEI", flush=True)
        
        # Create new buffer and send to RTP pipeline
        new_buffer = Gst.Buffer.new_wrapped(output_data)
        new_buffer.pts = buffer.pts
        new_buffer.dts = buffer.dts
        new_buffer.duration = buffer.duration
        new_buffer.set_flags(buffer.get_flags())
        
        ret = self.rtp_appsrc.emit("push-buffer", new_buffer)
        return Gst.FlowReturn.OK
    
    def on_detection_message(self, bus, message):
        """Handle detection pipeline messages"""
        t = message.type
        if t == Gst.MessageType.ERROR:
            err, dbg = message.parse_error()
            print(f"\n[DETECTION ERROR] {err}")
            if dbg:
                print(f"[DEBUG] {dbg}")
            self.stop()
        elif t == Gst.MessageType.EOS:
            print("\n[DETECTION] End of stream")
            self.stop()
    
    def on_transmission_message(self, bus, message):
        """Handle transmission pipeline messages"""
        t = message.type
        if t == Gst.MessageType.ERROR:
            err, dbg = message.parse_error()
            print(f"\n[TRANSMISSION ERROR] {err}")
            if dbg:
                print(f"[DEBUG] {dbg}")
        elif t == Gst.MessageType.STATE_CHANGED:
            if message.src == self.transmission_pipeline:
                old_state, new_state, pending = message.parse_state_changed()
                if new_state == Gst.State.PLAYING:
                    print("▶️  H.264 encoding started...")
    
    def on_rtp_message(self, bus, message):
        """Handle RTP pipeline messages"""
        t = message.type
        if t == Gst.MessageType.ERROR:
            err, dbg = message.parse_error()
            print(f"\n[RTP ERROR] {err}")
            if dbg:
                print(f"[DEBUG] {dbg}")
        elif t == Gst.MessageType.STATE_CHANGED:
            if message.src == self.rtp_pipeline:
                old_state, new_state, pending = message.parse_state_changed()
                if new_state == Gst.State.PLAYING:
                    print("📡 RTP transmission started...")
    
    def start(self):
        """Start the fixed tracking sender"""
        print("=" * 70)
        print("FIXED POSE TRACKING SENDER WITH DEBUG")
        print("=" * 70)
        print(f"📹 Camera: {self.device}")
        print(f"🧠 HEF Model: {self.hef}")
        print(f"⚙️  Post-process SO: {self.post_so}")
        print(f"🌐 Destination: {self.host}:{self.port}")
        print(f"📦 Resolution: {self.width}x{self.height} -> 1280x720")
        print(f"🔧 Hailo Python: {'Available' if HAVE_HAILO else 'Not Available'}")
        print(f"🆔 SEI UUID: {SEINALInjector.CUSTOM_UUID[:8].hex()}")
        print("=" * 70)
        
        self.running = True
        
        # Create pipelines
        self.create_detection_pipeline()
        self.create_transmission_pipeline()
        
        # Start pipelines in order
        print("Starting pipelines...")
        
        # Start RTP pipeline first
        ret = self.rtp_pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            print("ERROR: Unable to set RTP pipeline to PLAYING")
            sys.exit(1)
        
        # Start transmission pipeline
        ret = self.transmission_pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            print("ERROR: Unable to set transmission pipeline to PLAYING")
            sys.exit(1)
        
        # Start detection pipeline
        ret = self.detection_pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            print("ERROR: Unable to set detection pipeline to PLAYING")
            sys.exit(1)
        
        print("All pipelines started! Detecting and transmitting with SEI debug:")
        print("-" * 70)
        
        try:
            loop = GLib.MainLoop()
            loop.run()
        except KeyboardInterrupt:
            print(f"\n[INFO] Keyboard interrupt. Frames: {self.frame_counter}, SEI injections: {self.sei_injection_counter}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop all pipelines"""
        self.running = False
        
        print("[INFO] Stopping pipelines...")
        
        if self.detection_pipeline:
            self.detection_pipeline.set_state(Gst.State.NULL)
        if self.transmission_pipeline:
            self.transmission_pipeline.set_state(Gst.State.NULL)
        if self.rtp_pipeline:
            self.rtp_pipeline.set_state(Gst.State.NULL)
        
        print(f"[INFO] Session complete. Frames: {self.frame_counter}, SEI: {self.sei_injection_counter}")

def main():
    parser = argparse.ArgumentParser(
        description='Fixed pose tracking sender with working SEI injection and debug output',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Fixed version with proper SEI injection and detailed debug output.

Example:
  python fixed_tracking_sender.py --device /dev/video0 --host 127.0.0.1 --port 5000
        """
    )
    
    parser.add_argument("--device", default="/dev/video0", help="Video device path")
    parser.add_argument("--hef", default="./yolov8m_pose.hef", help="HEF model file")
    parser.add_argument("--post-so", default="./libyolov8pose_postprocess.so", help="Post-process SO file")
    parser.add_argument("--host", default="127.0.0.1", help="Destination IP address")
    parser.add_argument("--port", type=int, default=5000, help="UDP port")
    parser.add_argument("--width", type=int, default=640, help="Input width")
    parser.add_argument("--height", type=int, default=480, help="Input height")
    
    args = parser.parse_args()
    
    sender = FixedTrackingSender(
        device=args.device,
        hef=args.hef,
        post_so=args.post_so,
        host=args.host,
        port=args.port,
        width=args.width,
        height=args.height
    )
    
    sender.start()

if __name__ == "__main__":
    main()


