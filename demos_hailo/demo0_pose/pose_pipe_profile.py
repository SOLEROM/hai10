#!/usr/bin/env python3
import sys
import argparse
import gi

gi.require_version("Gst", "1.0")
gi.require_version("GObject", "2.0")
from gi.repository import Gst, GObject, GLib

Gst.init(None)


def build_pipeline(
    device="/dev/video0",
    width=1280,
    height=720,
    sensor_fps=60,
    process_fps=60,
    infer_width=640,
    infer_height=360,
    hef_path="./yolov8m_pose.hef",
    post_so="./libyolov8pose_postprocess.so",
    video_sink="xvimagesink",
):
    """
    Build profiling pipeline:

      - Capture at width x height (e.g. 1280x720)
      - Downscale to infer_width x infer_height before Hailo (e.g. 640x360)
      - fps_pre_hailo:  before hailonet (after downscale + convert)
      - fps_post_hailo: after hailotracker
      - hailo_display:  final display FPS
    """

    pipe = f"""
        hailomuxer name=hmux
        v4l2src device={device} name=source !
        video/x-raw,format=UYVY,width={width},height={height},framerate={sensor_fps}/1 !
        videorate drop-only=true !
        video/x-raw,framerate={process_fps}/1 !
        queue name=source_scale_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        videoscale name=source_videoscale n-threads=2 !
        queue name=source_convert_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        videoconvert n-threads=3 name=source_convert qos=false !
        video/x-raw,format=RGB,pixel-aspect-ratio=1/1 !
        queue name=inference_scale_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        videoscale name=inference_videoscale n-threads=2 qos=false !
        video/x-raw,width={infer_width},height={infer_height},pixel-aspect-ratio=1/1 !
        queue name=inference_convert_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
        video/x-raw,pixel-aspect-ratio=1/1 !
        videoconvert name=inference_videoconvert n-threads=2 !
        tee name=t_pre_hailo

        t_pre_hailo. !
          queue name=fps_pre_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
          fpsdisplaysink name=fps_pre_hailo
            video-sink=fakesink
            sync=false
            text-overlay=false
            signal-fps-measurements=true

        t_pre_hailo. !
          queue name=inference_hailonet_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
          hailonet name=inference_hailonet hef-path={hef_path} batch-size=1 force-writable=true !
          queue name=inference_hailofilter_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
          hailofilter name=inference_hailofilter so-path={post_so} function-name=filter qos=false !
          queue name=inference_hailotracker_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
          hailotracker name=hailo_tracker class-id=0 !
          tee name=t_post_hailo

        t_post_hailo. !
          queue name=fps_post_q leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 !
          fpsdisplaysink name=fps_post_hailo
            video-sink=fakesink
            sync=false
            text-overlay=false
            signal-fps-measurements=true

        t_post_hailo. !
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

def on_fps_pre(_sink, fps, droprate, avg_fps):
    print(f"[PRE HAILO]   fps={fps:6.2f}  drop={droprate:6.2f}  avg={avg_fps:6.2f}")


def on_fps_post(_sink, fps, droprate, avg_fps):
    print(f"[POST HAILO]  fps={fps:6.2f}  drop={droprate:6.2f}  avg={avg_fps:6.2f}")


def on_fps_display(_sink, fps, droprate, avg_fps):
    print(f"[DISPLAY]     fps={fps:6.2f}  drop={droprate:6.2f}  avg={avg_fps:6.2f}")


def run_pipeline(args, loop):
    pipeline_str = build_pipeline(
        device=args.device,
        width=args.width,
        height=args.height,
        sensor_fps=args.sensor_fps,
        process_fps=args.process_fps,
        infer_width=args.infer_width,
        infer_height=args.infer_height,
        hef_path=args.hef,
        post_so=args.post,
        video_sink=args.sink,
    )

    if args.print:
        print("=== PIPELINE ===")
        print(pipeline_str)
        return 0

    try:
        pipeline = Gst.parse_launch(pipeline_str)
    except GLib.GError as e:
        print(f"Failed to parse pipeline: {e}", file=sys.stderr)
        return 1

    # Helper to connect to fpsdisplaysink signals depending on version
    def connect_fps(name, callback):
        elem = pipeline.get_by_name(name)
        if not elem:
            print(f"WARNING: cannot find element '{name}'", file=sys.stderr)
            return
        # Prefer the newer "fps-measurements" signal
        try:
            elem.connect("fps-measurements", callback)
            return
        except TypeError:
            pass

        # Fallback: older single-arg "fps-measurement" signal
        def wrap(_sink, fps):
            callback(_sink, fps, 0.0, fps)

        try:
            elem.connect("fps-measurement", wrap)
        except TypeError:
            print(f"WARNING: '{name}' has no fps signals", file=sys.stderr)

    connect_fps("fps_pre_hailo", on_fps_pre)
    connect_fps("fps_post_hailo", on_fps_post)
    connect_fps("hailo_display", on_fps_display)

    # Bus handling
    bus = pipeline.get_bus()
    bus.add_signal_watch()

    def on_message(_bus, message):
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

    pipeline.set_state(Gst.State.PLAYING)
    print("Pipeline running. Ctrl+C to stop.\n")

    try:
        loop.run()
    except KeyboardInterrupt:
        print("\nStopping pipeline...")
    finally:
        pipeline.set_state(Gst.State.NULL)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hailo pose profiling pipeline (with downscale)")
    parser.add_argument("--device", default="/dev/video0")
    parser.add_argument("--width", type=int, default=1280, help="Capture width")
    parser.add_argument("--height", type=int, default=720, help="Capture height")
    parser.add_argument("--sensor-fps", type=int, default=60, help="Camera capture FPS")
    parser.add_argument("--process-fps", type=int, default=60, help="Processing target FPS via videorate")
    parser.add_argument("--infer-width", type=int, default=640, help="Width sent to Hailo")
    parser.add_argument("--infer-height", type=int, default=360, help="Height sent to Hailo")
    parser.add_argument("--hef", default="./yolov8m_pose.hef")
    parser.add_argument("--post", default="./libyolov8pose_postprocess.so")
    parser.add_argument("--sink", default="xvimagesink")
    parser.add_argument("--print", action="store_true", help="Print pipeline and exit")

    args = parser.parse_args()
    loop = GLib.MainLoop()
    sys.exit(run_pipeline(args, loop))


## usage example test:
# python3 pose_pipe_profile.py \
#  --width 1280 --height 720 \
#  --sensor-fps 60 --process-fps 60 \
#  --infer-width 640 --infer-height 640