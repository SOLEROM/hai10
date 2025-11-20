# simple save 2 file

## raw 

* simpl

```
gst-launch-1.0 -e -v \
  v4l2src device=/dev/video0 ! \
  video/x-raw,format=UYVY,width=1280,height=720,framerate=120/1 ! \
  queue ! \
  filesink sync=true async=false location=cam_720p120_uyvy.raw
```

* rec for 5 sec (120 fps * 5 sec = 600 frames)

```
gst-launch-1.0 -e -v \
  v4l2src device=/dev/video0 num-buffers=600 ! \
  video/x-raw,format=UYVY,width=1280,height=720,framerate=120/1 ! \
  queue ! \
  filesink sync=true async=false location=cam_720p120_uyvy.raw
```

* playback

```
gst-launch-1.0 -v \
  filesrc location=cam_720p120_uyvy.raw ! \
  videoparse format=uyvy width=1280 height=720 framerate=120/1 ! \
  videoconvert ! \
  autovideosink
```


* decode to avi:

```
ffmpeg -f rawvideo \
       -pixel_format uyvy422 \
       -video_size 1280x720 \
       -framerate 120 \
       -i cam_720p120_uyvy.raw \
       -c:v mjpeg cam_720p120_uyvy_mjpeg.avi
```


## avi container

* save as avi:

```
gst-launch-1.0 -e \
  v4l2src device=/dev/video0 ! \
  video/x-raw,format=UYVY,width=1280,height=720,framerate=120/1 ! \
  videoconvert ! video/x-raw,format=I420 ! \
  avimux ! filesink location=cam_720p120_uncompressed.avi
```

## store mJPG

* for 5 sec (114 fps * 5 sec = 570 frames)

```
gst-launch-1.0 -e -v \
  v4l2src device=/dev/video0 num-buffers=570 ! \
  image/jpeg,width=1920,height=1200,framerate=114/1 ! \
  avimux ! \
  filesink location=cam_1200p114.avi

```