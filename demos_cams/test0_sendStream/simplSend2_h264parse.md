## sender

gst-launch-1.0 -v \
  v4l2src device=/dev/video0 ! \
  video/x-raw,width=1280,height=720,framerate=120/1 ! \
  videoconvert ! \
  x264enc tune=zerolatency speed-preset=veryfast bitrate=4000 key-int-max=60 ! \
  h264parse ! \
  rtph264pay config-interval=1 pt=96 ! \
  udpsink host=HOST_IP port=5000

## receiver

gst-launch-1.0 -v \
  udpsrc port=5000 \
    caps="application/x-rtp, media=video, encoding-name=H264, clock-rate=90000, payload=96" ! \
  rtph264depay ! \
  h264parse ! \
  avdec_h264 ! \
  videoconvert ! \
  fpsdisplaysink video-sink=autovideosink text-overlay=true sync=false
