#!/usr/bin/env python3
import argparse
import os
import sys
import gi

gi.require_version("Gst", "1.0")
gi.require_version("GObject", "2.0")
from gi.repository import Gst, GLib

Gst.init(None)


def build_detection_pipeline(
    device="/dev/video0",
    width=640,
    height=480,
    input_fps=60,
    inference_fps=15,
    hef_path="./yolov8m.hef",
    post_so="./libyolo_hailortpp_post.so",
    network_name="yolov8m",
    batch_size=1,
    nms_score_threshold=0.3,
    nms_iou_threshold=0.45,
    input_source=None,          # file OR /dev/videoX OR None (default camera)
    segment_seconds=5.0,
    max_files=0,
    output_dir="./recordings",
    file_prefix="detRec_",
    bitrate_kbps=4000,
):
    """
    Build a GStreamer pipeline string for Hailo detection, writing
    overlaid output to segmented MP4 files (no display).

      source -> fps control -> hailonet -> hailofilter -> hailooverlay
            -> x264enc -> h264parse -> splitmuxsink
    """

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # File pattern for splitmuxsink, e.g. ./fly1/flyX00001.mp4
    file_pattern = os.path.join(output_dir, f"{file_prefix}%05d.mp4")
    segment_ns = int(segment_seconds * 1_000_000_000)

    # ---- Source element (camera vs file) ----
    if input_source:
        is_camera = input_source.startswith("/dev/video")
        if is_camera:
            source_element = f"v4l2src device={input_source} name=src_0 ! videoflip video-direction=horiz"
        else:
            source_element = f"filesrc location={input_source} name=src_0 ! decodebin"
    else:
        is_camera = True
        input_source = device
        source_element = f"v4l2src device={device} name=src_0 ! videoflip video-direction=horiz"

    # ---- FPS control (input vs inference) ----
    if is_camera:
        # Set camera caps to input_fps, then drop frames to inference_fps
        fps_block = (
            f" ! video/x-raw,format=UYVY,width={width},height={height},framerate={input_fps}/1 "
            f"! videorate drop-only=true ! video/x-raw,framerate={inference_fps}/1"
        )
    else:
        # For files, just enforce inference_fps
        fps_block = (
            f" ! videorate drop-only=true ! video/x-raw,framerate={inference_fps}/1"
        )

    thresholds_str = (
        f"nms-score-threshold={nms_score_threshold} "
        f"nms-iou-threshold={nms_iou_threshold} "
        f"output-format-type=HAILO_FORMAT_TYPE_FLOAT32"
    )

    # ---- Recording sink (encode + mux + segment) ----
    sink_element = f"""
        x264enc tune=zerolatency speed-preset=ultrafast bitrate={bitrate_kbps} key-int-max={inference_fps} !
        h264parse !
        splitmuxsink name=record_sink
            location={file_pattern}
            max-size-time={segment_ns}
            max-files={max_files}
            muxer-factory=mp4mux
    """

    pipe = f"""
        {source_element}
        {fps_block} !
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
    return " ".join(pipe.split())


def run_pipeline(args):
    pipeline_str = build_detection_pipeline(
        device=args.device,
        width=args.width,
        height=args.height,
        input_fps=args.input_fps,
        inference_fps=args.inference_fps,
        hef_path=args.hef,
        post_so=args.post,
        network_name=args.network,
        batch_size=args.batch_size,
        nms_score_threshold=args.nms_score,
        nms_iou_threshold=args.nms_iou,
        input_source=args.input,
        segment_seconds=args.segment_seconds,
        max_files=args.max_files,
        output_dir=args.output_dir,
        file_prefix=args.prefix,
        bitrate_kbps=args.bitrate,
    )

    if args.print:
        print("=== DETECTION PIPELINE (RECORDING) ===")
        print(pipeline_str)
        return 0

    print("=== CONFIG ===")
    print(f"Device:          {args.device}")
    print(f"Size:            {args.width}x{args.height}")
    print(f"Input FPS:       {args.input_fps}")
    print(f"Inference FPS:   {args.inference_fps}")
    print(f"Segment seconds: {args.segment_seconds}")
    print(f"Max files:       {args.max_files}")
    print(f"Output dir:      {args.output_dir}")
    print(f"Prefix:          {args.prefix}")
    print("================\n")

    pipeline = Gst.parse_launch(pipeline_str)

    # For debug: connect to splitmuxsink element messages (segment open/close)
    bus = pipeline.get_bus()
    bus.add_signal_watch()

    def on_message(bus, message):
        t = message.type
        if t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print(f"[ERROR] {err}", file=sys.stderr)
            if debug:
                print(f"[DEBUG] {debug}", file=sys.stderr)
            loop.quit()
        elif t == Gst.MessageType.EOS:
            print("[INFO] EOS reached, stopping main loop.")
            loop.quit()
        elif t == Gst.MessageType.ELEMENT:
            s = message.get_structure()
            if not s:
                return
            name = s.get_name()
            if name == "splitmuxsink-fragment-opened":
                loc = s.get_string("location")
                idx_ok, idx = s.get_uint("fragment-id")
                if not idx_ok:
                    idx = -1
                print(f"[record] Opened segment #{idx}: {loc}")
            elif name == "splitmuxsink-fragment-closed":
                loc = s.get_string("location")
                idx_ok, idx = s.get_uint("fragment-id")
                if not idx_ok:
                    idx = -1
                print(f"[record] Closed segment #{idx}: {loc}")

    bus.connect("message", on_message)

    # Auto-stop logic: after N segments worth of time, send EOS
    # total_duration = segment_seconds * max_files (+ small safety margin)
    if args.max_files > 0 and args.segment_seconds > 0:
        total_ms = int(args.segment_seconds * args.max_files * 1000) + 1000

        def send_eos():
            print(f"[INFO] Reached planned total duration (~{args.segment_seconds * args.max_files:.1f}s). Sending EOS...")
            pipeline.send_event(Gst.Event.new_eos())
            return False  # do not reschedule

        GLib.timeout_add(total_ms, send_eos)
        print(f"[INFO] Will auto-send EOS after ~{args.segment_seconds * args.max_files:.1f}s.")

    pipeline.set_state(Gst.State.PLAYING)
    print("Detection recording pipeline running. Ctrl+C to stop early.\n")

    try:
        loop.run()
    except KeyboardInterrupt:
        print("\n[INFO] KeyboardInterrupt received, sending EOS...")
        pipeline.send_event(Gst.Event.new_eos())
        # Let EOS message stop the loop
    finally:
        print("[INFO] Setting pipeline to NULL.")
        pipeline.set_state(Gst.State.NULL)
        print("[INFO] Pipeline stopped, exiting.")

    return 0


if __name__ == "__main__":
    loop = GLib.MainLoop()

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
        description="Hailo Detection Pipeline (camera/file) recording to segmented MP4 files"
    )

    # Source / camera-style args
    parser.add_argument("--device", default="/dev/video0",
                        help="Camera device to use (default: /dev/video0)")
    parser.add_argument("--width", type=int, default=640,
                        help="Camera width (default: 640)")
    parser.add_argument("--height", type=int, default=480,
                        help="Camera height (default: 480)")
    parser.add_argument("--input-fps", type=int, default=60,
                        help="Camera input FPS (default: 60)")
    parser.add_argument("--inference-fps", type=int, default=15,
                        help="FPS after videorate for inference (default: 15)")

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

    # Recording parameters
    parser.add_argument("--segment-seconds", type=float, default=5.0,
                        help="Length of each output file in seconds (default: 5.0)")
    parser.add_argument("--max-files", type=int, default=0,
                        help="Maximum number of files to keep and total segments to run "
                             "(0 = unlimited, no auto-stop; default: 0)")
    parser.add_argument("--output-dir", default="./recordings",
                        help="Directory to store output files (default: ./recordings)")
    parser.add_argument("--prefix", default="detRec_",
                        help="File name prefix (default: detRec_)")
    parser.add_argument("--bitrate", type=int, default=4000,
                        help="H.264 encoder bitrate in kbps (default: 4000)")

    # Utility
    parser.add_argument("--print", action="store_true",
                        help="Print pipeline and exit (do not run)")

    args = parser.parse_args()
    sys.exit(run_pipeline(args))
