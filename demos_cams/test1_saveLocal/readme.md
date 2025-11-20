# about

* for simple recording option see [simple saves](./simpSave2File.md)
* for interval recorder use the [intervalRecorder](./intervalRecorder.py)

* for example : 5-second clips at 120 fps, keep only last 10 files, stop after 100 files

```
python3 intervalRecorder.py \
  --resolution 1280x720 \
  --fps 120 \
  --duration 5 \
  --folder ./captures \
  --template camRec_ \
  --rotate-count 10 \
  --max-files 100

```

### playback

```
gst-launch-1.0 -v \
  filesrc location=????.raw ! \
  videoparse format=uyvy width=1280 height=720 framerate=120/1 ! \
  videoconvert ! \
  autovideosink

```