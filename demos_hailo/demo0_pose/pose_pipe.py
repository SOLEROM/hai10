#!/usr/bin/env python3
import argparse
import subprocess
import shlex


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
    """
    Build the full GStreamer pipeline string.
    """

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
        fpsdisplaysink name=hailo_display video-sink={video_sink} sync=false text-overlay=false signal-fps-measurements=true
    """

    # Minify: remove newlines, compress spaces
    pipeline_clean = " ".join(pipe.split())
    return pipeline_clean


def main():
    parser = argparse.ArgumentParser(description="Hailo Pose Pipeline")
    parser.add_argument("--device", default="/dev/video0")
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--input-fps", type=int, default=30)
    parser.add_argument("--inference-fps", type=int, default=8)
    parser.add_argument("--hef", default="./yolov8m_pose.hef")
    parser.add_argument("--post", default="./libyolov8pose_postprocess.so")
    parser.add_argument("--sink", default="xvimagesink")
    parser.add_argument("--print", action="store_true", help="Print pipeline only")

    args = parser.parse_args()

    pipeline = build_pipeline(
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
        print("\n=== FINAL PIPELINE ===")
        print(pipeline)
        return

    print("\nRunning GStreamer pipeline…\n")
    cmd = ["gst-launch-1.0"] + shlex.split(pipeline)
    subprocess.run(cmd)


if __name__ == "__main__":
    main()
