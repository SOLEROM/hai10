#!/usr/bin/env python3
import argparse
import math
import subprocess
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Raw UYVY recorder using gst-launch-1.0 with log-style rotation"
    )

    parser.add_argument(
        "--device",
        default="/dev/video0",
        help="V4L2 device path (default: /dev/video0)",
    )

    # Resolution (single string like 1280x720)
    parser.add_argument(
        "--resolution",
        default="1280x720",
        help="Resolution as WIDTHxHEIGHT (default: 1280x720)",
    )

    parser.add_argument(
        "--fps",
        type=int,
        default=120,
        help="Frames per second (default: 120)",
    )

    parser.add_argument(
        "--duration",
        type=float,
        default=5.0,
        help="Duration per file in seconds (default: 5.0)",
    )

    parser.add_argument(
        "--folder",
        default="./",
        help="Folder to store recordings (default: ./)",
    )

    parser.add_argument(
        "--template",
        default="camRec_",
        help="Base filename template (prefix). Files will be template + N (default: camRec_)",
    )

    parser.add_argument(
        "--extension",
        default="raw",
        help="File extension without dot (default: raw)",
    )

    parser.add_argument(
        "--rotate-count",
        type=int,
        default=None,
        help="Max number of files to keep on disk. "
             "If set, oldest file is deleted when limit exceeded. "
             "If not set, no rotation is performed.",
    )

    parser.add_argument(
        "--max-files",
        type=int,
        default=None,
        help="Total number of files to record before exiting. "
             "If not set, records indefinitely until interrupted.",
    )

    return parser.parse_args()


def parse_resolution(res_str):
    try:
        w_str, h_str = res_str.lower().split("x")
        width = int(w_str)
        height = int(h_str)
        if width <= 0 or height <= 0:
            raise ValueError
        return width, height
    except Exception:
        raise ValueError(f"Invalid resolution '{res_str}'. Use WIDTHxHEIGHT, e.g. 1280x720.")


def find_start_index(folder: Path, template: str, extension: str) -> int:
    """
    Look for existing files like <template><N>.<extension> and continue from max(N)+1.
    If none found, start from 1.
    """
    max_idx = 0
    pattern = f"{template}*.{extension}"
    for f in folder.glob(pattern):
        name = f.name
        if not name.startswith(template):
            continue
        # Strip prefix and extension
        rest = name[len(template):]
        if rest.endswith(f".{extension}"):
            rest = rest[: -len(f".{extension}")]
        if rest.isdigit():
            idx = int(rest)
            if idx > max_idx:
                max_idx = idx
    return max_idx + 1


def build_gst_command(device, width, height, fps, num_buffers, filepath):
    caps = f"video/x-raw,format=UYVY,width={width},height={height},framerate={fps}/1"

    cmd = [
        "gst-launch-1.0",
        "-e",
        "-v",
        "v4l2src",
        f"device={device}",
        f"num-buffers={num_buffers}",
        "!",
        caps,
        "!",
        "queue",
        "!",
        "filesink",
        "sync=true",
        "async=false",
        f"location={filepath}",
    ]
    return cmd


def main():
    args = parse_args()

    try:
        width, height = parse_resolution(args.resolution)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    # Prepare folder
    out_dir = Path(args.folder).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Determine starting index from existing files
    start_idx = find_start_index(out_dir, args.template, args.extension)

    # Calculate how many frames per file
    fps = args.fps
    duration = args.duration
    if fps <= 0 or duration <= 0:
        print("FPS and duration must be positive.", file=sys.stderr)
        sys.exit(1)

    num_buffers = int(round(fps * duration))
    if num_buffers <= 0:
        num_buffers = 1

    rotate_count = args.rotate_count
    max_files = args.max_files if args.max_files is not None else math.inf

    print("========================================")
    print(" Raw UYVY Recorder")
    print("========================================")
    print(f"Device      : {args.device}")
    print(f"Resolution  : {width}x{height}")
    print(f"FPS         : {fps}")
    print(f"Duration    : {duration} sec per file")
    print(f"Frames/file : {num_buffers}")
    print(f"Output dir  : {out_dir}")
    print(f"Template    : {args.template}<N>.{args.extension}")
    print(f"Rotate max  : {rotate_count if rotate_count is not None else 'no rotation'}")
    print(f"Max files   : {max_files if max_files != math.inf else 'no limit'}")
    print("========================================")

    recorded_files = []  # list of Path objects
    files_made = 0
    idx = start_idx

    try:
        while files_made < max_files:
            filename = f"{args.template}{idx}.{args.extension}"
            filepath = out_dir / filename

            print(f"\n[INFO] Recording file #{files_made + 1} → {filepath}")
            cmd = build_gst_command(
                device=args.device,
                width=width,
                height=height,
                fps=fps,
                num_buffers=num_buffers,
                filepath=str(filepath),
            )

            # Run gst-launch synchronously
            try:
                result = subprocess.run(
                    cmd,
                    check=False,
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                )
            except FileNotFoundError:
                print("Error: gst-launch-1.0 not found in PATH.", file=sys.stderr)
                sys.exit(1)

            if result.returncode != 0:
                print(f"[ERROR] gst-launch-1.0 failed with code {result.returncode}. "
                      f"Stopping.", file=sys.stderr)
                break

            # File done
            recorded_files.append(filepath)
            files_made += 1
            idx += 1

            # Handle rotation (log-style)
            if rotate_count is not None and len(recorded_files) > rotate_count:
                oldest = recorded_files.pop(0)
                try:
                    oldest.unlink()
                    print(f"[ROTATE] Deleted oldest file: {oldest}")
                except FileNotFoundError:
                    print(f"[ROTATE] Oldest file already missing: {oldest}")
                except Exception as e:
                    print(f"[ROTATE] Failed to delete {oldest}: {e}", file=sys.stderr)

        print("\n[INFO] Done. Recorded", files_made, "file(s).")

    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user. Exiting.")


if __name__ == "__main__":
    main()
