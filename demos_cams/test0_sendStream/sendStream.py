#!/usr/bin/env python3
import argparse
import subprocess
import shlex
import sys

def build_raw_sender(args):
    # gst-launch-1.0 -v \
    #   v4l2src device=/dev/video0 ! \
    #   video/x-raw,format=UYVY,width=1280,height=720,framerate=120/1 ! \
    #   queue ! \
    #   rtpvrawpay pt=96 ! \
    #   udpsink host=HOST_IP port=5000
    pipeline = [
        "gst-launch-1.0", "-v",
        "v4l2src", f"device={args.device}", "!",
        f"video/x-raw,format=UYVY,width={args.width},height={args.height},framerate={args.framerate}/1", "!",
        "queue", "!",
        "rtpvrawpay", "pt=96", "!",
        "udpsink", f"host={args.host}", f"port={args.port}",
    ]
    return pipeline

def build_raw_receiver(args):
    # gst-launch-1.0 -v \
    #   udpsrc port=5000 caps="application/x-rtp, media=video, encoding-name=RAW, ..." ! \
    #   rtpvrawdepay ! videoconvert ! fpsdisplaysink ...
    caps = (
        "application/x-rtp,"
        "media=(string)video,"
        "encoding-name=(string)RAW,"
        "clock-rate=(int)90000,"
        "sampling=(string)YCbCr-4:2:2,"
        "depth=(string)8,"
        f"width=(string){args.width},"
        f"height=(string){args.height},"
        "payload=(int)96"
    )

    pipeline = [
        "gst-launch-1.0", "-v",
        "udpsrc", f"port={args.port}", f"caps={caps}", "!",
        "rtpvrawdepay", "!",
        "videoconvert", "!",
        "fpsdisplaysink",
        "video-sink=autovideosink",
        f"text-overlay={'true' if args.text_overlay else 'false'}",
        f"sync={'true' if args.sync else 'false'}",
    ]
    return pipeline

def build_h264_sender(args):
    # gst-launch-1.0 -v \
    #   v4l2src device=/dev/video0 ! \
    #   video/x-raw,width=1280,height=720,framerate=120/1 ! \
    #   videoconvert ! \
    #   x264enc tune=zerolatency speed-preset=veryfast bitrate=4000 key-int-max=60 ! \
    #   h264parse ! \
    #   rtph264pay config-interval=1 pt=96 ! \
    #   udpsink host=HOST_IP port=5000
    pipeline = [
        "gst-launch-1.0", "-v",
        "v4l2src", f"device={args.device}", "!",
        f"video/x-raw,width={args.width},height={args.height},framerate={args.framerate}/1", "!",
        "videoconvert", "!",
        "x264enc",
        f"tune={args.tune}",
        f"speed-preset={args.speed_preset}",
        f"bitrate={args.bitrate}",
        f"key-int-max={args.key_int_max}", "!",
        "h264parse", "!",
        "rtph264pay", "config-interval=1", "pt=96", "!",
        "udpsink", f"host={args.host}", f"port={args.port}",
    ]
    return pipeline

def build_h264_receiver(args):
    # gst-launch-1.0 -v \
    #   udpsrc port=5000 caps="application/x-rtp, media=video, encoding-name=H264, clock-rate=90000, payload=96" ! \
    #   rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! fpsdisplaysink ...
    caps = "application/x-rtp,media=video,encoding-name=H264,clock-rate=90000,payload=96"

    pipeline = [
        "gst-launch-1.0", "-v",
        "udpsrc", f"port={args.port}", f"caps={caps}", "!",
        "rtph264depay", "!",
        "h264parse", "!",
        "avdec_h264", "!",
        "videoconvert", "!",
        "fpsdisplaysink",
        "video-sink=autovideosink",
        f"text-overlay={'true' if args.text_overlay else 'false'}",
        f"sync={'true' if args.sync else 'false'}",
    ]
    return pipeline

def pipeline_to_cmd(pipeline):
    return " ".join(shlex.quote(x) for x in pipeline)

def print_counter_side(role, codec, args):
    """
    When we run sender, print the matching receiver command and vice versa.
    """
    if role == "sender":
        other_role = "receiver"
    else:
        other_role = "sender"

    if codec == "raw":
        if other_role == "sender":
            pipe = build_raw_sender(args)
        else:
            pipe = build_raw_receiver(args)
    else:  # h264
        if other_role == "sender":
            pipe = build_h264_sender(args)
        else:
            pipe = build_h264_receiver(args)

    print("\n===================================================")
    print(f"✨ Matching {other_role.upper()} GStreamer command ({codec}):")
    print("---------------------------------------------------")
    print(pipeline_to_cmd(pipe))
    print("===================================================\n")

def main():
    parser = argparse.ArgumentParser(
        description="Simple camera RTP stream tool (RAW / H.264) using GStreamer."
    )

    # High-level role + codec
    parser.add_argument(
        "--role",
        choices=["sender", "receiver"],
        default="sender",
        help="Run as sender (camera → network) or receiver (network → display).",
    )
    parser.add_argument(
        "--receiver",
        action="store_true",
        help="Shortcut: same as --role receiver.",
    )
    parser.add_argument(
        "--codec",
        choices=["raw", "h264"],
        default="h264",
        help="Stream codec: raw (UYVY over RTP) or h264.",
    )

    # Common video params
    parser.add_argument("--device", default="/dev/video0",
                        help="Video4Linux2 device for sender (default: /dev/video0).")
    parser.add_argument("--width", type=int, default=1280,
                        help="Frame width (default: 1280).")
    parser.add_argument("--height", type=int, default=720,
                        help="Frame height (default: 720).")
    parser.add_argument("--framerate", type=int, default=120,
                        help="Framerate numerator (default: 120 -> 120/1).")

    # Network params
    parser.add_argument("--host", default="127.0.0.1",
                        help="Destination IP/hostname for sender (default: 127.0.0.1).")
    parser.add_argument("--port", type=int, default=5000,
                        help="UDP port for sender/receiver (default: 5000).")

    # H.264-specific
    parser.add_argument("--bitrate", type=int, default=4000,
                        help="x264enc bitrate in kbps (default: 4000).")
    parser.add_argument("--key-int-max", type=int, default=60,
                        help="x264enc key-int-max (default: 60).")
    parser.add_argument("--tune", default="zerolatency",
                        help="x264enc tune (default: zerolatency).")
    parser.add_argument("--speed-preset", default="veryfast",
                        help="x264enc speed-preset (default: veryfast).")

    # Receiver display options
    parser.add_argument("--no-text-overlay", dest="text_overlay",
                        action="store_false",
                        help="Disable FPS text overlay on receiver.")
    parser.add_argument("--text-overlay", dest="text_overlay",
                        action="store_true",
                        help="Enable FPS text overlay on receiver (default).")
    parser.set_defaults(text_overlay=True)

    parser.add_argument("--sync", dest="sync",
                        action="store_true",
                        help="Enable sync on fpsdisplaysink (default: disabled).")
    parser.add_argument("--no-sync", dest="sync",
                        action="store_false",
                        help="Disable sync on fpsdisplaysink.")
    parser.set_defaults(sync=False)

    # Misc
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the gst-launch command and exit (do not run).")

    args = parser.parse_args()

    # Handle --receiver shortcut
    if args.receiver:
        args.role = "receiver"

    # Build pipeline according to role+codec
    if args.codec == "raw":
        if args.role == "sender":
            pipeline = build_raw_sender(args)
        else:
            pipeline = build_raw_receiver(args)
    else:  # h264
        if args.role == "sender":
            pipeline = build_h264_sender(args)
        else:
            pipeline = build_h264_receiver(args)

    cmd_str = pipeline_to_cmd(pipeline)

    print("===================================================")
    print(f"🎥 Running as {args.role.upper()} | codec={args.codec}")
    print("---------------------------------------------------")
    print(cmd_str)
    print("===================================================")

    # Print matching command for the other side
    print_counter_side(args.role, args.codec, args)

    if args.dry_run:
        print("Dry-run requested, not executing pipeline.")
        sys.exit(0)

    try:
        # Run GStreamer pipeline
        subprocess.run(pipeline, check=False)
    except KeyboardInterrupt:
        print("\nInterrupted by user, exiting...")

if __name__ == "__main__":
    main()
