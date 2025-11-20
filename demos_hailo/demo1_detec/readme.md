# About

## based on the

* https://github.com/hailo-ai/tappas/tree/v3.31.0/apps/h8/gstreamer/general/detection

```
gst-launch-1.0 filesrc location=/proj/tappas/swCenterDW/tappas_v3.29.1/apps/h8/gstreamer/general/detection/resources/detection.mp4 name=src_0 ! decodebin ! queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! videoscale qos=false n-threads=2 ! video/x-raw, pixel-aspect-ratio=1/1 ! queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! videoconvert n-threads=2 qos=false ! queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! hailonet hef-path=/proj/tappas/swCenterDW/tappas_v3.29.1/apps/h8/gstreamer/general/detection/resources/yolov8m.hef batch-size=1 nms-score-threshold=0.3 nms-iou-threshold=0.45 output-format-type=HAILO_FORMAT_TYPE_FLOAT32 ! queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! hailofilter function-name=yolov8m so-path=/proj/tappas/swCenterDW/tappas_v3.29.1/apps/h8/gstreamer/libs/post_processes//libyolo_hailortpp_post.so config-path=null qos=false ! queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! hailooverlay qos=false ! queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! videoconvert n-threads=2 qos=false ! queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! fpsdisplaysink video-sink=xvimagesink text-overlay=false name=hailo_display sync=false -v | grep -e hailo_display -e hailodevicestats

```

## 


```
# Default camera detection
python detection.py

# Different camera and resolution
python detection.py --device /dev/video0 --width 1280 --height 720 --input-fps 60

# Use a file instead of camera
python  detection.py --input /path/to/video.mp4

# Just print the gst-launch pipeline
python  detection.py --print

```