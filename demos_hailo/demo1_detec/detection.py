#!/usr/bin/env python3
import argparse
import os
import sys
import gi

gi.require_version("Gst", "1.0")
gi.require_version("GObject", "2.0")
from gi.repository import Gst, GObject

Gst.init(None)


def build_detection_pipeline(
    device="/dev/video0",
    width=640,
    height=480,
    input_fps=30,
    hef_path="./yolov8m.hef",
    post_so="./libyolo_hailortpp_post.so",
    network_name="yolov8m",
    batch_size=1,
    nms_score_threshold=0.3,
    nms_iou_threshold=0.45,
    video_sink="xvimagesink",
    input_source=None,          # if provided, can be file OR /dev/videoX
    tcp_host=None,
    tcp_port=None,
):
    """
    Build a GStreamer pipeline string for Hailo detection.
    By default works on a raw camera (v4l2src), like your pose example.
    """

    # ---- Source element (camera vs file) ----
    if input_source:
        # If user explicitly passes a source; detect if it's camera or file
        if input_source.startswith("/dev/video"):
            source_element = f"v4l2src device={input_source} name=src_0 ! videoflip video-direction=horiz"
        else:
            # file source
            source_element = f"filesrc location={input_source} name=src_0 ! decodebin"
    else:
        # Default: raw camera like pose script
        source_element = f"v4l2src device={device} name=src_0 ! videoflip video-direction=horiz"

    # Optional caps for camera (for files, caps will be negotiated by decodebin)
    camera_caps = ""
    if not input_source or (input_source and input_source.startswith("/dev/video")):
        camera_caps = (
            f" ! video/x-raw,format=UYVY,width={width},height={height},framerate={input_fps}/1"
        )

    # ---- Sink element (screen or TCP) ----
    if tcp_host and tcp_port:
        # For TAPPAS GUI-style TCP sink
        sink_element = f"""
            queue name=queue_before_sink leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 !
            videoscale !
            video/x-raw,width=836,height=546,format=RGB !
            tcpclientsink host={tcp_host} port={tcp_port}
        """
    else:
        # Local display with FPS output
        sink_element = f"""
            fpsdisplaysink name=hailo_display
                video-sink={video_sink}
                text-overlay=false
                sync=false
                signal-fps-measurements=true
        """

    thresholds_str = (
        f"nms-score-threshold={nms_score_threshold} "
        f"nms-iou-threshold={nms_iou_threshold} "
        f"output-format-type=HAILO_FORMAT_TYPE_FLOAT32"
    )

    pipe = f"""
        {source_element}
        {camera_caps} !
        queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 !
        videoscale qos=false n-threads=2 !
        video/x-raw,pixel-aspect-ratio=1/1 !
        queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 !
        videoconvert n-threads=2 qos=false !
        queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 !
        hailonet hef-path={hef_path} batch-size={batch_size} {thresholds_str} !
        queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 !
        hailofilter function-name={network_name} so-path={post_so} config-path=null qos=false !
        queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 !
        hailooverlay qos=false !
        queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 !
        videoconvert n-threads=2 qos=false !
        queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 !
        {sink_element}
    """
    # Clean whitespace into a single-line pipeline string
    return " ".join(pipe.split())


# -------- FPS callbacks --------
def on_fps_measurements(fpssink, fps, droprate, avg_fps):
    # signal: fps-measurements (double fps, double droprate, double avg_fps)
    print(f"[FPS] inst: {fps:.2f}  drop: {droprate:.2f}  avg: {avg_fps:.2f}")


def on_fps_measurement(fpssink, fps):
    # older signal: fps-measurement (double fps)
    print(f"[FPS] inst: {fps:.2f}")


def run_pipeline(args):
    pipeline_str = build_detection_pipeline(
        device=args.device,
        width=args.width,
        height=args.height,
        input_fps=args.input_fps,
        hef_path=args.hef,
        post_so=args.post,
        network_name=args.network,
        batch_size=args.batch_size,
        nms_score_threshold=args.nms_score,
        nms_iou_threshold=args.nms_iou,
        video_sink=args.sink,
        input_source=args.input,
        tcp_host=args.tcp_host,
        tcp_port=args.tcp_port,
    )

    if args.print:
        print("=== DETECTION PIPELINE ===")
        print(pipeline_str)
        return 0

    pipeline = Gst.parse_launch(pipeline_str)

    # Connect FPS signals (when using fpsdisplaysink)
    fpssink = pipeline.get_by_name("hailo_display")
    if fpssink:
        try:
            fpssink.connect("fps-measurements", on_fps_measurements)
        except TypeError:
            pass
        try:
            fpssink.connect("fps-measurement", on_fps_measurement)
        except TypeError:
            pass
    else:
        if not (args.tcp_host and args.tcp_port):
            print("Warning: fpsdisplaysink 'hailo_display' not found; no FPS output.", file=sys.stderr)

    # Bus handling
    bus = pipeline.get_bus()
    bus.add_signal_watch()

    def on_message(bus, message):
        t = message.type
        if t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print(f"ERROR: {err}", file=sys.stderr)
            if debug:
                print(f"DEBUG: {debug}", file=sys.stderr)
            loop.quit()
        elif t == Gst.MessageType.EOS:
            print("EOS reached")
            loop.quit()

    bus.connect("message", on_message)

    # Start pipeline
    pipeline.set_state(Gst.State.PLAYING)
    print("Detection pipeline running. Ctrl+C to stop.")

    try:
        loop.run()
    except KeyboardInterrupt:
        print("\nStopping pipeline...")
    finally:
        pipeline.set_state(Gst.State.NULL)

    return 0


if __name__ == "__main__":
    GObject.threads_init()
    loop = GObject.MainLoop()

    # Try to use TAPPAS env paths for nicer defaults, if present
    tappas_ws = os.environ.get("TAPPAS_WORKSPACE", "")
    if tappas_ws:
        default_post = os.path.join(
            tappas_ws,
            "apps", "h8", "gstreamer", "libs", "post_processes",
            "libyolo_hailortpp_post.so",
        )
        default_hef = os.path.join(
            tappas_ws,
            "apps", "h8", "gstreamer", "general", "detection", "resources",
            "yolov8m.hef",
        )
    else:
        default_post = "./libyolo_hailortpp_post.so"
        default_hef = "./yolov8m.hef"

    parser = argparse.ArgumentParser(
        description="Hailo Detection Pipeline (camera/file) with FPS print"
    )

    # Source / camera-style args (like your pose script)
    parser.add_argument("--device", default="/dev/video0",
                        help="Camera device to use (default: /dev/video0)")
    parser.add_argument("--width", type=int, default=640,
                        help="Camera width (default: 640)")
    parser.add_argument("--height", type=int, default=480,
                        help="Camera height (default: 480)")
    parser.add_argument("--input-fps", type=int, default=30,
                        help="Camera input FPS (default: 30)")

    # Optional input override (file or another /dev/videoX)
    parser.add_argument("--input", "-i", default=None,
                        help="If set, use this as source (file path or /dev/videoX)")

    # Network / Hailo bits
    parser.add_argument("--hef", default=default_hef,
                        help=f"Path to HEF file (default: {default_hef})")
    parser.add_argument("--post", default=default_post,
                        help=f"Path to postprocess .so (default: {default_post})")
    parser.add_argument("--network", default="yolov8m",
                        help="Network name for hailofilter function-name (default: yolov8m)")
    parser.add_argument("--batch-size", type=int, default=1,
                        help="Hailonet batch size (default: 1)")
    parser.add_argument("--nms-score", type=float, default=0.3,
                        help="NMS score threshold (default: 0.3)")
    parser.add_argument("--nms-iou", type=float, default=0.45,
                        help="NMS IoU threshold (default: 0.45)")

    # Sink
    parser.add_argument("--sink", default="xvimagesink",
                        help="Video sink for local display (default: xvimagesink)")
    parser.add_argument("--tcp-host", default=None,
                        help="If set with --tcp-port, send frames to TCP host instead of local sink")
    parser.add_argument("--tcp-port", type=int, default=None,
                        help="TCP port for tcpclientsink (requires --tcp-host)")

    # Utility
    parser.add_argument("--print", action="store_true",
                        help="Print pipeline and exit (do not run)")

    args = parser.parse_args()
    sys.exit(run_pipeline(args))
