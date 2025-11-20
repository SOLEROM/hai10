#!/usr/bin/env python3
import argparse
import sys

import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GObject, GLib


def build_pipeline(args):
    """
    Build a GStreamer pipeline equivalent to:

    gst-launch-1.0 \
      filesrc location=... ! \
      decodebin ! queue ! videoscale ! ... ! hailonet ! hailofilter ! hailooverlay ! \
      videoconvert ! x264enc ! rtph264pay ! udpsink ...
    """

    pipeline_str = f"""
        filesrc location="{args.input}" name=src_0 !
        decodebin !
        queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 !
        videoscale qos=false n-threads=2 !
        video/x-raw,pixel-aspect-ratio=1/1 !
        queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 !
        videoconvert n-threads=2 qos=false !
        queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 !
        hailonet hef-path="{args.hef}"
                 batch-size=1
                 nms-score-threshold=0.3
                 nms-iou-threshold=0.45
                 output-format-type=HAILO_FORMAT_TYPE_FLOAT32 !
        queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 !
        hailofilter function-name="{args.function}"
                    so-path="{args.post}"
                    config-path="{args.config}"
                    qos=false !
        queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 !
        hailooverlay qos=false !
        queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 !
        videoconvert n-threads=2 qos=false !
        x264enc tune=zerolatency
                 speed-preset=ultrafast
                 bitrate={args.bitrate}
                 key-int-max=30 !
        rtph264pay config-interval=1 pt=96 !
        udpsink host="{args.host}" port={args.port}
    """

    # Strip leading spaces so parse_launch is happy
    pipeline_str = "\n".join(line.strip() for line in pipeline_str.splitlines() if line.strip())
    print("Using pipeline:\n", pipeline_str, "\n")

    pipeline = Gst.parse_launch(pipeline_str)
    return pipeline


def main():
    parser = argparse.ArgumentParser(
        description="Hailo detection pipeline: file → Hailo → H264/RTP → UDP"
    )

    # Defaults are your original paths
    parser.add_argument(
        "--input",
        default="/local/tappas/tappas-3.30.0/apps/h8/gstreamer/rockchip/detection/resources/detection.mp4",
        help="Input video file path",
    )
    parser.add_argument(
        "--hef",
        default="/local/tappas/tappas-3.30.0/apps/h8/gstreamer/rockchip/detection/resources/yolov5m_wo_spp_60p.hef",
        help="Path to HEF model file",
    )
    parser.add_argument(
        "--post",
        default="/local/tappas/tappas-3.30.0/apps/h8/gstreamer/libs/post_processes/libyolo_hailortpp_post.so",
        help="Path to post-process .so library",
    )
    parser.add_argument(
        "--config",
        default="/local/tappas/tappas-3.30.0/apps/h8/gstreamer/rockchip/detection/resources/configs/yolov5.json",
        help="Path to post-process JSON config",
    )
    parser.add_argument(
        "--function",
        default="yolov5",
        help="Function name inside the post-process .so",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Destination IP for UDP stream",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Destination UDP port",
    )
    parser.add_argument(
        "--bitrate",
        type=int,
        default=4000,
        help="Video bitrate (kbps) for x264enc",
    )

    args = parser.parse_args()

    Gst.init(None)

    pipeline = build_pipeline(args)

    # Bus handling
    bus = pipeline.get_bus()
    bus.add_signal_watch()

    def on_message(bus, message, loop):
        msg_type = message.type
        if msg_type == Gst.MessageType.EOS:
            print("EOS received, stopping pipeline.")
            pipeline.set_state(Gst.State.NULL)
            loop.quit()
        elif msg_type == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print(f"ERROR from {message.src.get_name()}: {err}", file=sys.stderr)
            if debug:
                print(f"Debug info: {debug}", file=sys.stderr)
            pipeline.set_state(Gst.State.NULL)
            loop.quit()

    loop = GLib.MainLoop()
    bus.connect("message", on_message, loop)

    print("Starting pipeline...")
    pipeline.set_state(Gst.State.PLAYING)

    try:
        loop.run()
    except KeyboardInterrupt:
        print("Interrupted by user, stopping...")
    finally:
        pipeline.set_state(Gst.State.NULL)


if __name__ == "__main__":
    main()

