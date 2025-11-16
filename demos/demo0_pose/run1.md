# About

Here’s what that monster does, step by step, from camera to screen.

---

### 1. Capture from the camera

```bash
v4l2src device=/dev/video0 name=source !
video/x-raw,format=UYVY,width=640,height=480,framerate=30/1 !
```

* `v4l2src`: reads raw video frames from `/dev/video0`.
* Caps filter forces:

  * Format: `UYVY` (YUV 4:2:2)
  * Resolution: `640x480`
  * FPS: `30 fps`

So: **640×480 @ 30 fps UYVY** from the camera.

---

### 2. Reduce framerate for processing

```bash
videorate drop-only=true !
video/x-raw,framerate=8/1 !
```

* `videorate drop-only=true`: only drops frames, never duplicates.
* Caps: `framerate=8/1` → keep about 8 fps, drop the rest.

So: you still capture at 30 fps, but **only send 8 fps onward** to save NPU/CPU.

---

### 3. Pre-scale before color conversion

```bash
queue name=source_scale_q ... !
videoscale name=source_videoscale n-threads=2 !
queue name=source_convert_q ... !
videoconvert n-threads=3 name=source_convert qos=false !
video/x-raw,format=RGB,pixel-aspect-ratio=1/1 !
```

* `queue` elements:

  * Break threads, decouple stages, store up to 3 buffers each.
  * `leaky=no` → if downstream is slow, pipeline will backpressure (not drop).
* `videoscale`: resizes frames if needed (even if you didn’t set explicit size here, later caps may impose constraints).
* `videoconvert`: converts from `UYVY` to `RGB`.
* Caps: `video/x-raw,format=RGB,pixel-aspect-ratio=1/1`:

  * Enforce **RGB** (what Hailo expects).
  * Ensure square pixels (aspect ratio 1:1).

Now we have **RGB frames at 8 fps**, ready for inference pre-scaling.

---

### 4. Inference-oriented scaling & cleanup

```bash
queue name=inference_scale_q ... !
videoscale name=inference_videoscale n-threads=2 qos=false !
queue name=inference_convert_q ... !
video/x-raw,pixel-aspect-ratio=1/1 !
videoconvert name=inference_videoconvert n-threads=2 !
```

* Another `queue` + `videoscale` pair:

  * Typically used to scale to the exact **network input resolution** (e.g., 640×640, 640×384, etc., depending on the HEF).
* Caps: again forcing square pixels.
* `videoconvert` again:

  * Ensures final format/colorspace exactly match what `hailonet` wants
    (some Hailo plugins are picky about memory layout and color formats).

Think of this block as: **"massage the frame into exactly what the HEF needs"**.

---

### 5. Run the Hailo neural network (YOLOv8 pose)

```bash
queue name=inference_hailonet_q ... !
hailonet name=inference_hailonet \
    hef-path=./yolov8m_pose.hef \
    batch-size=1 \
    force-writable=true !
```

* `hailonet`:

  * Loads your Hailo model from `yolov8m_pose.hef`.
  * Runs **inference on the Hailo accelerator**.
  * `batch-size=1`: infer one frame at a time.
  * `force-writable=true`: ensures buffers are writable for downstream (handy when some plugins need to modify metadata or data).

This stage converts **RGB frames → tensors → network outputs + Hailo metadata** attached to buffers.

---

### 6. Post-process neural network outputs

```bash
queue name=inference_hailofilter_q ... !
hailofilter name=inference_hailofilter \
    so-path=./libyolov8pose_postprocess.so \
    function-name=filter qos=false !
```

* `hailofilter`:

  * Loads a custom post-processing shared object: `libyolov8pose_postprocess.so`.
  * Calls the function `filter` inside that `.so` for each frame.
* This is where raw NN outputs (heatmaps, etc.) are turned into:

  * keypoints / skeletons
  * boxes
  * confidences
  * and packaged into **Hailo metadata** on the buffer.

So: **raw NN output → meaningful pose results.**

---

### 7. Track objects / people over time

```bash
queue name=inference_hailotracker_q ... !
hailotracker name=hailo_tracker class-id=0 !
```

* `hailotracker`:

  * Reads metadata from `hailofilter`.
  * Assigns **track IDs** over time (who is person #1, #2, etc.).
  * `class-id=0`: track only detections of class 0 (usually “person”).

So you get **temporal tracking**, not just per-frame detections.

---

### 8. Identity element for callbacks / probes

```bash
queue name=identity_callback_q ... !
identity name=identity_callback !
```

* `identity`:

  * Pass-through element that does nothing to the buffer.
  * Common trick: you attach **probes** or signal handlers here in your code to:

    * read metadata
    * log results
    * send data over network
  * The name `identity_callback` hints you probably connect some C/Python signal to it.

Think: **hook point for your app logic.**

---

### 9. Draw overlays (skeletons / boxes)

```bash
queue name=hailo_display_hailooverlay_q ... !
hailooverlay name=hailo_display_hailooverlay !
```

* `hailooverlay`:

  * Reads tracking + pose metadata.
  * Draws **visual overlay**: bounding boxes, skeleton, labels, etc. directly onto the frame.

This is where the magic becomes visible. 🕺

---

### 10. Convert for display and show with FPS

```bash
queue name=hailo_display_videoconvert_q ... !
videoconvert name=hailo_display_videoconvert n-threads=2 qos=false !
queue name=hailo_display_q ... !
fpsdisplaysink name=hailo_display \
    video-sink=xvimagesink \
    sync=false \
    text-overlay=false \
    signal-fps-measurements=true
```

* `videoconvert`: convert into whatever format the display sink (`xvimagesink`) prefers.
* `fpsdisplaysink`:

  * Wraps a sink (here `xvimagesink`) and measures FPS.
  * `video-sink=xvimagesink`: actual display is Xv accelerated window.
  * `sync=false`: run as fast as upstream provides frames (no syncing to clock).
  * `text-overlay=false`: don’t draw FPS text on top.
  * `signal-fps-measurements=true`: emit signals with FPS data (so your app can log it).

So this block is your **visual output + performance monitor**.

---

