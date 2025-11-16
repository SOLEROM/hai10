# About


## deps

```

sudo apt update
sudo apt install --no-install-recommends \
  gstreamer1.0-tools \
  gstreamer1.0-plugins-base \
  gstreamer1.0-plugins-good \
  gstreamer1.0-plugins-bad \
  gstreamer1.0-plugins-ugly \
  gstreamer1.0-libav
```

## sender

```
python  trackSender.py --device /dev/video0 --host 10.0.0.50 --port 5000

```

```
💉 Inserted SEI at position 46 (before IDR)
✅ SEI injection #15 successful! New size: 84860 bytes
🔍 After injection NALUs: [9, 7, 8, 6, 5, 5, 5, 5]
🎬 H.264 frame: NALUs [9, 1, 1, 1, 1], Keyframe: False, Size: 13598 bytes
🎯 Frame 114: 1 objects detected
📊 Tracking data queued: Frame 114, Objects 1
🎬 H.264 frame: NALUs [9, 1, 1, 1, 1], Keyframe: False, Size: 19926 bytes
🎯 Frame 115: 1 objects detected
📊 Tracking data queued: Frame 115, Objects 1
🎬 H.264 frame: NALUs [9, 1, 1, 1, 1], Keyframe: False, Size: 24667 bytes
🎯 Frame 116: 1 objects detected
📊 Tracking data queued: Frame 116, Objects 1
🎬 H.264 frame: NALUs [9, 1, 1, 1, 1], Keyframe: False, Size: 22412 bytes
🎯 Frame 117: 1 objects detected
📊 Tracking data queued: Frame 117, Objects 1
🎬 H.264 frame: NALUs [9, 1, 1, 1, 1], Keyframe: False, Size: 28311 bytes
🎯 Frame 118: 1 objects detected
📊 Tracking data queued: Frame 118, Objects 1
🎬 H.264 frame: NALUs [9, 1, 1, 1, 1], Keyframe: False, Size: 26944 bytes
🎯 Frame 119: 1 objects detected
📊 Tracking data queued: Frame 119, Objects 1
🎬 H.264 frame: NALUs [9, 1, 1, 1, 1], Keyframe: False, Size: 25742 bytes
🎯 Frame 120: 1 objects detected
📊 Tracking data queued: Frame 120, Objects 1
🎬 H.264 frame: NALUs [9, 7, 8, 5, 5, 5, 5], Keyframe: True, Size: 93399 bytes
🎯 Frame 121: 1 objects detected


```

## receiver 

```
python3 trackReceiver.py 5000 --display
```

```
🔍 Processing buffer #121
🔍 Stream format detected: avc, buffer size: 93479 bytes
🔍 Found 8 NAL units
  📍 NAL #0: AUD (type 9) at 0, size 2
  📍 NAL #1: SPS (type 7) at 6, size 28
  📍 NAL #2: PPS (type 8) at 38, size 4
  📍 NAL #3: SEI (type 6) at 46, size 76
  📍 NAL #4: IDR (type 5) at 126, size 19622
  📍 NAL #5: IDR (type 5) at 19752, size 24593
  📍 NAL #6: IDR (type 5) at 44349, size 27421
  📍 NAL #7: IDR (type 5) at 71774, size 21701
🎯 Processing SEI NAL #1 at position 46
📦 SEI payload size: 75 bytes
🔍 SEI payload preview: 054853494d545241434b00000000000000007b226672616d65223a3131322c22
📋 Processing SEI message #1 at offset 0
  📊 Message type: 5, size: 72
  🎯 user_data_unregistered found, size: 72
  🆔 UUID in payload: 53494d545241434b0000000000000000
  🆔 Expected UUID:   53494d545241434b0000000000000000
  ✅ UUID match! Extracting JSON data...
  📝 JSON string: {"frame":112,"objects":1,"timestamp":1758995225.8887086}
  🎉 Successfully parsed metadata: {'frame': 112, 'objects': 1, 'timestamp': 1758995225.8887086}
🎯 Buffer #121 contains valid SEI data!

```
user@user-Latitude-5440:~/proj/id3/v1$ cat README.md 
# Real-Time Pose Tracking with SEI Metadata Transmission

A complete system for real-time pose detection using Hailo AI accelerators with embedded tracking metadata transmitted via H.264 SEI (Supplemental Enhancement Information) over RTP/UDP.

## Overview

This system consists of two main components:

1. **Sender** (`fixed_tracking_sender.py`) - Captures video, performs pose detection with Hailo, and transmits H.264 video with embedded tracking metadata
2. **Receiver** (`multi_format_receiver.py`) - Receives the video stream and extracts tracking metadata from SEI NAL units

The tracking data (frame numbers, object counts, timestamps) is embedded directly into the H.264 video stream using SEI NAL units, ensuring metadata stays synchronized with the video frames.

## Features

- ✅ Real-time pose detection using Hailo AI accelerators
- ✅ Object tracking with frame-by-frame metadata
- ✅ SEI NAL unit injection for metadata embedding
- ✅ Multi-format H.264 stream support (byte-stream and AVC)
- ✅ RTP/UDP transmission for low-latency streaming
- ✅ Comprehensive debugging and monitoring
- ✅ Live video display and optional recording

## Requirements

### Hardware
- Camera device (USB webcam, CSI camera, etc.)
- Hailo AI accelerator (for pose detection)
- Network connection between sender and receiver

### Software Dependencies
```bash
# GStreamer with development headers
sudo apt-get install gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-libav

# Python GStreamer bindings
pip install PyGObject

# Hailo Python API (if available)
# Follow Hailo documentation for installation
```

### Required Files
- `yolov8m_pose.hef` - Hailo pose detection model
- `libyolov8pose_postprocess.so` - Post-processing library

## Usage

### 1. Sender (Transmitting Device)

```bash
python fixed_tracking_sender.py [OPTIONS]
```

#### Sender Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--device` | `/dev/video0` | Video capture device path |
| `--hef` | `./yolov8m_pose.hef` | Path to Hailo model file |
| `--post-so` | `./libyolov8pose_postprocess.so` | Path to post-processing library |
| `--host` | `127.0.0.1` | Destination IP address |
| `--port` | `5000` | UDP port for transmission |
| `--width` | `640` | Input video width |
| `--height` | `480` | Input video height |

#### Sender Examples

```bash
# Basic usage with default settings
python fixed_tracking_sender.py

# Send to remote host
python fixed_tracking_sender.py --host 192.168.1.100 --port 5000

# Use different camera and resolution
python fixed_tracking_sender.py --device /dev/video1 --width 1280 --height 720

# Custom model files
python fixed_tracking_sender.py --hef /path/to/model.hef --post-so /path/to/postprocess.so
```

### 2. Receiver (Receiving Device)

```bash
python multi_format_receiver.py PORT [OPTIONS]
```

#### Receiver Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `PORT` | ✅ | UDP port to listen on (must match sender) |
| `--display` | ❌ | Enable live video display |
| `--save-video FILE` | ❌ | Save received video to file (MP4) |
| `--no-display` | ❌ | Explicitly disable display |

#### Receiver Examples

```bash
# Basic usage with display
python multi_format_receiver.py 5000 --display

# Save video without display
python multi_format_receiver.py 5000 --save-video output.mp4

# Both display and save
python multi_format_receiver.py 5000 --display --save-video recording.mp4

# No display (metadata extraction only)
python multi_format_receiver.py 5000 --no-display
```

## Complete Workflow Example

### Step 1: Start the Receiver
```bash
# On the receiving machine (IP: 192.168.1.100)
python multi_format_receiver.py 5000 --display
```

### Step 2: Start the Sender
```bash
# On the sending machine (with camera and Hailo)
python fixed_tracking_sender.py --host 192.168.1.100 --port 5000
```

## Output and Monitoring

### Sender Output
The sender provides detailed debug information:

```
🎯 Frame 104: 1 objects detected
📊 Tracking data queued: Frame 104, Objects 1
🎬 H.264 frame: NALUs [9, 7, 8, 5, 5, 5, 5], Keyframe: True, Size: 103984 bytes
📝 Creating SEI: Frame 95, Objects 1
📦 SEI NAL size: 79 bytes, UUID: 53494d545241434b
💉 Inserted SEI at position 46 (before IDR)
✅ SEI injection #14 successful! New size: 104063 bytes
🔍 After injection NALUs: [9, 7, 8, 6, 5, 5, 5, 5]
```

### Receiver Output
The receiver shows successful metadata extraction:

```
🔍 Stream format detected: avc, buffer size: 104063 bytes
🔍 Found 8 NAL units
  📍 NAL #3: SEI (type 6) at 46, size 79
🎯 Processing SEI NAL #1 at position 46
✅ UUID match! Extracting JSON data...
📝 JSON string: {"frame":95,"objects":1,"timestamp":1730646723.456}

==================================================
🎯 TRACKING DATA #014
==================================================
📍 Frame Number: 0095
👥 Object Count: 01
⏰ Timestamp: 1730646723.456
⏱️  Runtime: 15.2s
📊 Total Objects: 23
==================================================
```

## Metadata Format

The embedded tracking metadata is JSON formatted:

```json
{
  "frame": 95,        // Frame number from detection pipeline
  "objects": 1,       // Number of objects detected in this frame
  "timestamp": 1730646723.456  // Unix timestamp when data was created
}
```

## Technical Details

### SEI NAL Unit Structure
- **NAL Type**: 6 (SEI)
- **Message Type**: 5 (user_data_unregistered)
- **UUID**: `SIMTRACK` + 8 null bytes
- **Payload**: JSON tracking data
- **Termination**: RBSP stop bit (0x80)

### Stream Formats Supported
- **Byte-stream**: Uses start codes (`00 00 00 01`)
- **AVC**: Uses length-prefixed NAL units
- **Auto-detection**: Automatically handles format conversion

### Network Protocol
- **Transport**: UDP (low latency)
- **Encapsulation**: RTP (Real-time Transport Protocol)
- **Payload**: H.264 with embedded SEI metadata

## Troubleshooting

### No Video Stream
```bash
# Check camera availability
ls /dev/video*

# Test camera with GStreamer
gst-launch-1.0 v4l2src device=/dev/video0 ! videoconvert ! xvimagesink
```

### Network Issues
```bash
# Check if port is available
sudo netstat -ulnp | grep 5000

# Test network connectivity
ping [RECEIVER_IP]

# Check firewall (Ubuntu/Debian)
sudo ufw status
```

### No SEI Data Received
1. Verify sender is injecting SEI (look for ✅ SEI injection messages)
2. Check UUID matches between sender and receiver
3. Ensure no firewalls blocking UDP traffic
4. Verify port numbers match

### Hailo Detection Issues
1. Check model file exists and is readable
2. Verify post-processing library is compatible
3. Ensure Hailo runtime is properly installed
4. Check camera permissions

### Performance Optimization
```bash
# Sender optimizations
--width 640 --height 480  # Lower resolution for better performance
--width 1280 --height 720  # Higher resolution for better quality

# Network optimizations
# Use wired connection for best results
# Minimize network hops between sender and receiver
```

## File Structure

```
tracking-system/
├── fixed_tracking_sender.py      # Main sender application
├── multi_format_receiver.py      # Main receiver application
├── README.md                     # This documentation
├── yolov8m_pose.hef              # Hailo pose detection model
└── libyolov8pose_postprocess.so  # Post-processing library
```

## Advanced Configuration

### Custom Video Parameters
```bash
# High quality streaming
python fixed_tracking_sender.py --width 1920 --height 1080

# High frame rate (adjust encoder settings in code)
# Modify key-int-max and bitrate parameters
```

### Multiple Receivers
The sender can broadcast to multiple receivers by using broadcast addresses or running multiple sender instances with different hosts.

### Recording and Playback
```bash
# Record received stream
python multi_format_receiver.py 5000 --save-video session.mp4

# Later analysis of recorded files can extract SEI metadata
```

