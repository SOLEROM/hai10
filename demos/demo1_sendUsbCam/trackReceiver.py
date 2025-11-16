#!/usr/bin/env python3
"""
multi_format_receiver.py - H.264 receiver that handles both byte-stream and AVC formats
Enhanced to detect SEI in different H.264 stream formats
Usage: python multi_format_receiver.py 5000 --display
"""

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import sys
import json
import argparse
import time
import struct

class MultiFormatSEIExtractor:
    """SEI extractor that handles both byte-stream and AVC formats"""
    
    CUSTOM_UUID = b'SIMTRACK' + b'\x00' * 8  # Custom UUID for simple tracking data
    
    @staticmethod
    def detect_stream_format(data):
        """Detect if stream is byte-stream or AVC format"""
        if len(data) < 8:
            return "unknown"
        
        # Check for byte-stream start codes
        if data[:4] == b'\x00\x00\x00\x01' or data[:3] == b'\x00\x00\x01':
            return "byte-stream"
        
        # Check for AVC format (length-prefixed)
        if len(data) >= 4:
            nal_length = struct.unpack('>I', data[:4])[0]
            if 0 < nal_length < len(data) and nal_length + 4 <= len(data):
                return "avc"
        
        return "unknown"
    
    @staticmethod
    def parse_byte_stream_nalus(data):
        """Parse NAL units in byte-stream format"""
        nalus = []
        i = 0
        
        while i < len(data) - 4:
            start_code_len = 0
            if data[i:i+4] == b'\x00\x00\x00\x01':
                start_code_len = 4
            elif data[i:i+3] == b'\x00\x00\x01':
                start_code_len = 3
            else:
                i += 1
                continue
            
            # Find next start code or end of data
            end = len(data)
            for j in range(i + start_code_len, len(data) - 2):
                if data[j:j+4] == b'\x00\x00\x00\x01' or data[j:j+3] == b'\x00\x00\x01':
                    end = j
                    break
            
            if i + start_code_len < len(data):
                nal_type = data[i + start_code_len] & 0x1F
                nal_data = data[i + start_code_len:end]
                nalus.append((i, nal_type, nal_data))
            
            i = end
        
        return nalus
    
    @staticmethod
    def parse_avc_nalus(data):
        """Parse NAL units in AVC/length-prefixed format"""
        nalus = []
        i = 0
        
        while i < len(data) - 4:
            try:
                # Read NAL length
                nal_length = struct.unpack('>I', data[i:i+4])[0]
                
                if nal_length <= 0 or i + 4 + nal_length > len(data):
                    break
                
                nal_data = data[i+4:i+4+nal_length]
                if nal_data:
                    nal_type = nal_data[0] & 0x1F
                    nalus.append((i, nal_type, nal_data))
                
                i += 4 + nal_length
                
            except (struct.error, IndexError):
                break
        
        return nalus
    
    @staticmethod
    def find_and_extract_sei(data):
        """Extract SEI from data, auto-detecting format"""
        extracted = []
        
        # Detect stream format
        stream_format = MultiFormatSEIExtractor.detect_stream_format(data)
        print(f"🔍 Stream format detected: {stream_format}, buffer size: {len(data)} bytes", flush=True)
        
        # Parse NAL units based on format
        if stream_format == "byte-stream":
            nalus = MultiFormatSEIExtractor.parse_byte_stream_nalus(data)
        elif stream_format == "avc":
            nalus = MultiFormatSEIExtractor.parse_avc_nalus(data)
        else:
            print(f"❌ Unknown stream format, trying both parsers...", flush=True)
            # Try both parsers
            nalus = MultiFormatSEIExtractor.parse_byte_stream_nalus(data)
            if not nalus:
                nalus = MultiFormatSEIExtractor.parse_avc_nalus(data)
        
        print(f"🔍 Found {len(nalus)} NAL units", flush=True)
        
        # Show NAL unit summary
        for i, (pos, nal_type, nal_data) in enumerate(nalus[:10]):  # Show first 10
            nal_names = {1: "P-slice", 5: "IDR", 6: "SEI", 7: "SPS", 8: "PPS", 9: "AUD"}
            nal_name = nal_names.get(nal_type, f"Type-{nal_type}")
            print(f"  📍 NAL #{i}: {nal_name} (type {nal_type}) at {pos}, size {len(nal_data)}", flush=True)
        
        # Process SEI NAL units
        sei_count = 0
        for pos, nal_type, nal_data in nalus:
            if nal_type == 6:  # SEI
                sei_count += 1
                print(f"🎯 Processing SEI NAL #{sei_count} at position {pos}", flush=True)
                
                try:
                    extracted_from_sei = MultiFormatSEIExtractor.extract_from_sei_payload(nal_data[1:])  # Skip NAL header
                    extracted.extend(extracted_from_sei)
                except Exception as e:
                    print(f"❌ Error processing SEI: {e}", flush=True)
        
        if sei_count == 0:
            print("❌ No SEI NAL units found", flush=True)
        
        return extracted
    
    @staticmethod
    def extract_from_sei_payload(sei_payload):
        """Extract tracking data from SEI payload"""
        extracted = []
        
        print(f"📦 SEI payload size: {len(sei_payload)} bytes", flush=True)
        print(f"🔍 SEI payload preview: {sei_payload[:32].hex() if len(sei_payload) >= 32 else sei_payload.hex()}", flush=True)
        
        # Parse SEI messages
        k = 0
        payload_count = 0
        
        while k < len(sei_payload) - 1:
            payload_count += 1
            print(f"📋 Processing SEI message #{payload_count} at offset {k}", flush=True)
            
            # Read payload type
            payload_type = 0
            while k < len(sei_payload) and sei_payload[k] == 0xFF:
                payload_type += 255
                k += 1
            if k < len(sei_payload):
                payload_type += sei_payload[k]
                k += 1
            
            # Read payload size
            payload_size = 0
            while k < len(sei_payload) and sei_payload[k] == 0xFF:
                payload_size += 255
                k += 1
            if k < len(sei_payload):
                payload_size += sei_payload[k]
                k += 1
            
            print(f"  📊 Message type: {payload_type}, size: {payload_size}", flush=True)
            
            # Check for user_data_unregistered (type 5)
            if payload_type == 5 and k + payload_size <= len(sei_payload):
                payload = sei_payload[k:k+payload_size]
                
                print(f"  🎯 user_data_unregistered found, size: {len(payload)}", flush=True)
                
                # Check for our UUID
                if len(payload) >= 16:
                    uuid_in_payload = payload[:16]
                    expected_uuid = MultiFormatSEIExtractor.CUSTOM_UUID
                    
                    print(f"  🆔 UUID in payload: {uuid_in_payload.hex()}", flush=True)
                    print(f"  🆔 Expected UUID:   {expected_uuid.hex()}", flush=True)
                    
                    if uuid_in_payload == expected_uuid:
                        print("  ✅ UUID match! Extracting JSON data...", flush=True)
                        
                        try:
                            json_data = payload[16:].rstrip(b'\x00\x80')
                            json_str = json_data.decode('utf-8')
                            print(f"  📝 JSON string: {json_str}", flush=True)
                            
                            metadata = json.loads(json_str)
                            print(f"  🎉 Successfully parsed metadata: {metadata}", flush=True)
                            extracted.append(metadata)
                            
                        except (UnicodeDecodeError, json.JSONDecodeError) as e:
                            print(f"  ❌ JSON parsing error: {e}", flush=True)
                    else:
                        print("  ❌ UUID mismatch - not our tracking data", flush=True)
                else:
                    print(f"  ❌ Payload too short for UUID: {len(payload)} bytes", flush=True)
                
                k += payload_size
            else:
                print(f"  ⏭️  Skipping message type {payload_type}", flush=True)
                if payload_type != 5 and k + payload_size <= len(sei_payload):
                    k += payload_size
                else:
                    break
        
        return extracted

class MultiFormatReceiver:
    def __init__(self, port, display=True, save_video=None):
        self.port = port
        self.display = display
        self.save_video = save_video
        self.pipeline = None
        
        # Statistics
        self.sei_count = 0
        self.buffer_count = 0
        self.sei_buffer_count = 0
        self.last_frame_num = 0
        self.total_objects_seen = 0
        self.start_time = time.time()
        
        Gst.init(None)
    
    def on_pad_probe(self, pad, info):
        """Multi-format probe with enhanced SEI extraction"""
        buffer = info.get_buffer()
        if not buffer:
            return Gst.PadProbeReturn.OK
        
        self.buffer_count += 1
        
        try:
            # Get buffer data
            success, map_info = buffer.map(Gst.MapFlags.READ)
            if not success:
                return Gst.PadProbeReturn.OK
            
            data = bytes(map_info.data)
            buffer.unmap(map_info)
            
            print(f"\n🔍 Processing buffer #{self.buffer_count}", flush=True)
            
            # Extract SEI metadata with multi-format support
            extracted_list = MultiFormatSEIExtractor.find_and_extract_sei(data)
            
            if extracted_list:
                self.sei_buffer_count += 1
                print(f"🎯 Buffer #{self.buffer_count} contains valid SEI data!", flush=True)
            
            for tracking_data in extracted_list:
                self.sei_count += 1
                print(f"\n🎉 SEI extraction #{self.sei_count} successful!", flush=True)
                
                # Print tracking information
                self.print_tracking_data(tracking_data)
                
        except Exception as e:
            print(f"❌ Error in probe: {e}", flush=True)
        
        return Gst.PadProbeReturn.OK
    
    def print_tracking_data(self, tracking_data):
        """Print tracking information"""
        frame_num = tracking_data.get('frame', 0)
        object_count = tracking_data.get('objects', 0)
        timestamp = tracking_data.get('timestamp', 0)
        
        runtime = time.time() - self.start_time
        
        # Update statistics
        self.last_frame_num = frame_num
        self.total_objects_seen += object_count
        
        print("=" * 50)
        print(f"🎯 TRACKING DATA #{self.sei_count:03d}")
        print("=" * 50)
        print(f"📍 Frame Number: {frame_num:04d}")
        print(f"👥 Object Count: {object_count:02d}")
        print(f"⏰ Timestamp: {timestamp:.3f}")
        print(f"⏱️  Runtime: {runtime:.1f}s")
        print(f"📊 Total Objects: {self.total_objects_seen}")
        print("=" * 50)
    
    def create_pipeline(self):
        """Create pipeline with multiple probe points for debugging"""
        pipeline_parts = [
            f"udpsrc port={self.port} caps=\"application/x-rtp,media=video,encoding-name=H264,payload=96\" !",
            "rtph264depay name=depay !",
            "h264parse name=parse config-interval=-1 !",
            "tee name=t"
        ]
        
        # Add display branch if requested
        if self.display:
            pipeline_parts.extend([
                "t. !",
                "queue !",
                "avdec_h264 !",
                "videoconvert !",
                "videoscale !",
                "video/x-raw,width=1280,height=720 !",
                "fpsdisplaysink name=display video-sink=xvimagesink sync=false text-overlay=true signal-fps-measurements=true"
            ])
        
        # Add file saving branch if requested
        if self.save_video:
            pipeline_parts.extend([
                "t. !",
                "queue !",
                "mp4mux !",
                f"filesink location={self.save_video}"
            ])
        
        # Add fakesink if no other sinks
        if not self.display and not self.save_video:
            pipeline_parts.extend([
                "t. !",
                "queue !",
                "fakesink"
            ])
        
        pipeline_str = " ".join(pipeline_parts)
        
        try:
            self.pipeline = Gst.parse_launch(pipeline_str)
        except GLib.GError as e:
            print(f"Error creating pipeline: {e}")
            sys.exit(1)
        
        # Add probes at multiple points for debugging
        
        # Probe after RTP depayloader
        depay = self.pipeline.get_by_name('depay')
        if depay:
            src_pad = depay.get_static_pad('src')
            if src_pad:
                src_pad.add_probe(
                    Gst.PadProbeType.BUFFER,
                    lambda pad, info: self.debug_probe(pad, info, "after-depay")
                )
                print("✅ Debug probe added after RTP depayloader")
        
        # Main probe after h264parse
        parse = self.pipeline.get_by_name('parse')
        if parse:
            src_pad = parse.get_static_pad('src')
            if src_pad:
                src_pad.add_probe(
                    Gst.PadProbeType.BUFFER,
                    self.on_pad_probe
                )
                print("✅ Main SEI probe added after h264parse")
        
        # Set up bus
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
    
    def debug_probe(self, pad, info, location):
        """Debug probe to show format at different pipeline points"""
        buffer = info.get_buffer()
        if not buffer:
            return Gst.PadProbeReturn.OK
        
        success, map_info = buffer.map(Gst.MapFlags.READ)
        if success:
            data = bytes(map_info.data)
            buffer.unmap(map_info)
            
            format_type = MultiFormatSEIExtractor.detect_stream_format(data)
            print(f"🔧 Debug {location}: {len(data)} bytes, format: {format_type}", flush=True)
            
            # Show first few bytes
            preview = data[:16].hex() if len(data) >= 16 else data.hex()
            print(f"   Preview: {preview}", flush=True)
        
        return Gst.PadProbeReturn.OK
    
    def on_message(self, bus, message):
        """Handle pipeline messages"""
        t = message.type
        
        if t == Gst.MessageType.EOS:
            print(f"\n✅ Stream complete. SEI packets received: {self.sei_count}")
            self.print_final_statistics()
            self.stop()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print(f"\n❌ Error: {err}, {debug}")
            self.stop()
        elif t == Gst.MessageType.STATE_CHANGED:
            if message.src == self.pipeline:
                old_state, new_state, pending = message.parse_state_changed()
                if new_state == Gst.State.PLAYING:
                    print("▶️  Multi-format receiver started...")
    
    def print_final_statistics(self):
        """Print final statistics"""
        runtime = time.time() - self.start_time
        
        print("\n" + "=" * 60)
        print("📊 FINAL MULTI-FORMAT STATISTICS")
        print("=" * 60)
        print(f"⏱️  Runtime: {runtime:.1f} seconds")
        print(f"📦 Total buffers processed: {self.buffer_count}")
        print(f"📋 Buffers with valid SEI: {self.sei_buffer_count}")
        print(f"💉 SEI packets extracted: {self.sei_count}")
        print(f"🎯 Last frame number: {self.last_frame_num}")
        print(f"👥 Total objects detected: {self.total_objects_seen}")
        
        if self.buffer_count > 0:
            sei_rate = (self.sei_buffer_count / self.buffer_count) * 100
            print(f"📈 SEI success rate: {sei_rate:.1f}%")
        
        print("=" * 60)
    
    def start(self):
        """Start the multi-format receiver"""
        print("=" * 60)
        print("MULTI-FORMAT H.264 TRACKING RECEIVER")
        print("=" * 60)
        print(f"📡 UDP port: {self.port}")
        print(f"📺 Display: {'Enabled' if self.display else 'Disabled'}")
        print(f"💾 Save video: {self.save_video if self.save_video else 'Disabled'}")
        print(f"🔍 UUID: {MultiFormatSEIExtractor.CUSTOM_UUID.hex()}")
        print("🔧 Supports: byte-stream and AVC formats")
        print("=" * 60)
        
        self.create_pipeline()
        
        ret = self.pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            print("Unable to set pipeline to playing state")
            sys.exit(1)
        
        self.loop = GLib.MainLoop()
        
        # Add timeout
        self.timeout_id = GLib.timeout_add_seconds(25, self.check_timeout)
        
        try:
            self.loop.run()
        except KeyboardInterrupt:
            print("\n⏹️  Interrupted by user")
            self.print_final_statistics()
            self.stop()
    
    def check_timeout(self):
        """Check timeout with enhanced feedback"""
        if self.buffer_count == 0:
            print("\n⏱️  Timeout - no data received")
            self.stop()
            return False
        elif self.sei_count > 0:
            print(f"\n✅ Receiving SEI data successfully! ({self.sei_count} packets)")
            return False
        else:
            print(f"\n⏳ Still trying... {self.buffer_count} buffers processed, {self.sei_buffer_count} with SEI")
            return True
    
    def stop(self):
        """Stop the receiver"""
        if hasattr(self, 'timeout_id'):
            GLib.source_remove(self.timeout_id)
        
        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)
        
        if hasattr(self, 'loop') and self.loop:
            self.loop.quit()
        
        print("🛑 Multi-format receiver stopped")

def main():
    parser = argparse.ArgumentParser(
        description='Multi-format H.264 receiver with enhanced SEI detection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Enhanced receiver that handles both byte-stream and AVC H.264 formats.

Examples:
  python multi_format_receiver.py 5000 --display
  python multi_format_receiver.py 5000 --save-video output.mp4
        """
    )
    
    parser.add_argument('port', type=int, help='UDP port to receive on')
    parser.add_argument('--display', action='store_true', help='Display live video')
    parser.add_argument('--save-video', help='Save video to file (MP4)')
    
    args = parser.parse_args()
    
    if args.port < 1024 or args.port > 65535:
        print("Error: Port must be between 1024 and 65535")
        sys.exit(1)
    
    if not args.display and not args.save_video:
        args.display = True
    
    receiver = MultiFormatReceiver(args.port, args.display, args.save_video)
    receiver.start()

if __name__ == '__main__':
    main()

