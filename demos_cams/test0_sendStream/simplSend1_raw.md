## sender

gst-launch-1.0 -v \
  v4l2src device=/dev/video0 ! \
  video/x-raw,format=UYVY,width=1280,height=720,framerate=120/1 ! \
  queue ! \
  rtpvrawpay pt=96 ! \
  udpsink host=HOST_IP port=5000

## receiver

gst-launch-1.0 -v \
  udpsrc port=5000 caps="application/x-rtp, \
    media=(string)video, \
    encoding-name=(string)RAW, \
    clock-rate=(int)90000, \
    sampling=(string)YCbCr-4:2:2, \
    depth=(string)8, \
    width=(string)1280, \
    height=(string)720, \
    payload=(int)96" ! \
  rtpvrawdepay ! \
  videoconvert ! \
  fpsdisplaysink video-sink=autovideosink text-overlay=true sync=false