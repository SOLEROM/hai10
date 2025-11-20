#!/usr/bin/env python3
import argparse
import sys
import gi

gi.require_version("Gst", "1.0")
gi.require_version("GObject", "2.0")
from gi.repository import Gst, GObject

Gst.init(None)


def build_pipeline(
    device="/dev/video0",
    width=640,
    height=480,
    input_fps=30,
    inference_fps=8,
    hef_path="./yolov8m_pose.hef",
    post_so="./libyolov8pose_postprocess.so",
    video_sink="xvimagesink",
):
    pipe = f"""
        hailomuxer name=hmux

        v4l2src device={device} name=source !
        video/x-raw,format=UYVY,width={width},height={height},framerate={input_fps}/1 !
        videorate drop-only=true !
        video/x-raw,framerate={inference_fps}/1 !

        queue name=source_scale_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        videoscale name=source_videoscale n-threads=2 !
        queue name=source_convert_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        videoconvert n-threads=3 name=source_convert qos=false !
        video/x-raw,format=RGB,pixel-aspect-ratio=1/1 !

        queue name=inference_scale_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        videoscale name=inference_videoscale n-threads=2 qos=false !
        queue name=inference_convert_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        video/x-raw,pixel-aspect-ratio=1/1 !
        videoconvert name=inference_videoconvert n-threads=2 !

        queue name=inference_hailonet_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        hailonet name=inference_hailonet hef-path={hef_path} batch-size=1 force-writable=true !

        queue name=inference_hailofilter_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        hailofilter name=inference_hailofilter so-path={post_so} function-name=filter qos=false !

        queue name=inference_hailotracker_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        hailotracker name=hailo_tracker class-id=0 !

        queue name=identity_callback_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        identity name=identity_callback !

        queue name=hailo_display_hailooverlay_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        hailooverlay name=hailo_display_hailooverlay !

        queue name=hailo_display_videoconvert_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        videoconvert name=hailo_display_videoconvert n-threads=2 qos=false !

        queue name=hailo_display_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        fpsdisplaysink name=hailo_display
            video-sink={video_sink}
            sync=false
            text-overlay=false
            signal-fps-measurements=true
    """
    return " ".join(pipe.split())


# -------- FPS callbacks --------

def on_fps_measurements(fpssink, fps, droprate, avg_fps):
    # signal: fps-measurements (double fps, double droprate, double avg_fps)
    print(f"FPS: {fps:.2f}  drop: {droprate:.2f}  avg: {avg_fps:.2f}")


def on_fps_measurement(fpssink, fps):
    # older signal: fps-measurement (double fps)
    print(f"FPS: {fps:.2f}")


def run_pipeline(args):
    pipeline_str = build_pipeline(
        device=args.device,
        width=args.width,
        height=args.height,
        input_fps=args.input_fps,
        inference_fps=args.inference_fps,
        hef_path=args.hef,
        post_so=args.post,
        video_sink=args.sink,
    )

    if args.print:
        print("=== PIPELINE ===")
        print(pipeline_str)
        return 0

    pipeline = Gst.parse_launch(pipeline_str)

    # Connect FPS signals
    fpssink = pipeline.get_by_name("hailo_display")
    if not fpssink:
        print("Could not find fpsdisplaysink element 'hailo_display'", file=sys.stderr)
    else:
        # Try both signals (depends on your GStreamer version)
        try:
            fpssink.connect("fps-measurements", on_fps_measurements)
        except TypeError:
            pass
        try:
            fpssink.connect("fps-measurement", on_fps_measurement)
        except TypeError:
            pass

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
    print("Pipeline running. Ctrl+C to stop.")

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

    parser = argparse.ArgumentParser(description="Hailo Pose Pipeline with FPS print")
    parser.add_argument("--device", default="/dev/video0")
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--input-fps", type=int, default=30)
    parser.add_argument("--inference-fps", type=int, default=8)
    parser.add_argument("--hef", default="./yolov8m_pose.hef")
    parser.add_argument("--post", default="./libyolov8pose_postprocess.so")
    parser.add_argument("--sink", default="xvimagesink")
    parser.add_argument("--print", action="store_true", help="Print pipeline and exit")

    args = parser.parse_args()
    sys.exit(run_pipeline(args))
