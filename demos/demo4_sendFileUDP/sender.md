gst-launch-1.0 \
  filesrc location=/local/tappas/tappas-3.30.0/apps/h8/gstreamer/rockchip/detection/resources/detection.mp4 name=src_0 ! \
  decodebin ! \
  queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! \
  videoscale qos=false n-threads=2 ! \
  video/x-raw, pixel-aspect-ratio=1/1 ! \
  queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! \
  videoconvert n-threads=2 qos=false ! \
  queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! \
  hailonet hef-path=/local/tappas/tappas-3.30.0/apps/h8/gstreamer/rockchip/detection/resources/yolov5m_wo_spp_60p.hef \
          batch-size=1 nms-score-threshold=0.3 nms-iou-threshold=0.45 output-format-type=HAILO_FORMAT_TYPE_FLOAT32 ! \
  queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! \
  hailofilter function-name=yolov5 \
              so-path=/local/tappas/tappas-3.30.0/apps/h8/gstreamer/libs/post_processes//libyolo_hailortpp_post.so \
              config-path=/local/tappas/tappas-3.30.0/apps/h8/gstreamer/rockchip/detection/resources/configs/yolov5.json \
              qos=false ! \
  queue leaky=no max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! \
  hailooverlay qos=false ! \
  queue leaky=no max-size-buffers=30 max-size-buffers=30 max-size-bytes=0 max-size-time=0 ! \
  videoconvert n-threads=2 qos=false ! \
  x264enc tune=zerolatency speed-preset=ultrafast bitrate=4000 key-int-max=30 ! \
  rtph264pay config-interval=1 pt=96 ! \
  udpsink host=<IP>  port=5000



