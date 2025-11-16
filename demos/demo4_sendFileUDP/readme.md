# file pipe sender over udp 


file → decode → preprocess → Hailo NN → postprocess → overlay → H264 encode → RTP → UDP.




## receiver:

```
gst-launch-1.0  udpsrc port=5000 caps="application/x-rtp, media=video, encoding-name=H264, clock-rate=90000, payload=96" !   rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink sync=false

```

## sender:

```
python3 hailo_udp_pipeline.py \
  --input /data/my_video.mp4 \
  --hef /models/my_yolo.hef \
  --post /libs/libmy_post.so \
  --config /configs/my_yolo.json \
  --host 192.168.1.50 \
  --port 6000 \
  --bitrate 6000

```

Here is the **full explanation of the pipeline you gave**, step-by-step, from **file → decode → preprocess → Hailo NN → postprocess → overlay → H264 encode → RTP → UDP**.


---

# 🟦 **1. Input video from file**

```bash
filesrc location=/local/.../detection.mp4 name=src_0 !
decodebin !
```

* `filesrc` reads an MP4 file from disk.
* `decodebin` automatically detects and loads the correct decoder:

  * H.264 → h264parse → v4l2h264dec (Rockchip)
  * H.265 → appropriate decoders
  * etc.

➡️ Output is a **raw video stream**, e.g. `video/x-raw` in some YUV or RGB color format.

---

# 🟦 **2. Preprocessing (scale + convert)**

### Queue #1

```bash
queue leaky=no max-size-buffers=30 ...
```

* Decouples decoding thread from preprocessing thread.
* Large buffer size because reading from file is bursty.

---

### Scale the frame

```bash
videoscale qos=false n-threads=2 !
video/x-raw, pixel-aspect-ratio=1/1 !
```

* `videoscale`: resize frames (even if not forced — ensures consistent geometry).
* Par=1/1 → square pixels.

➡️ Ensures frame is normalized before Hailo inference.

---

### Queue #2

```bash
queue leaky=no max-size-buffers=30 ...
```

Keeps everything stable even if CPU spikes.

---

### Convert colorspace

```bash
videoconvert n-threads=2 qos=false !
```

Hailo inference almost always expects **RGB**.

* If decoder outputs NV12/YUYV/I420, this converts it.

➡️ Converts raw video into the **format the network expects**.

---

### Queue #3

```bash
queue leaky=no max-size-buffers=30 ...
```

Buffers between CPU and NPU.

---

# 🟦 **3. Hailo Neural Network inference**

```bash
hailonet hef-path=.../yolov5m_wo_spp_60p.hef \
         batch-size=1
         nms-score-threshold=0.3
         nms-iou-threshold=0.45
         output-format-type=HAILO_FORMAT_TYPE_FLOAT32 !
```

This is the **Hailo NPU engine**.

It takes the raw video frame → runs inference using the HEF.

* `batch-size=1` → process one frame at a time (default for video).
* Score & IoU thresholds → NMS is done internally.
* Output format FP32 → ensures post-process `.so` supports it.

👉 Output is **video frame + raw neural-network metadata attached to buffer**.

---

### Queue #4

Isolates the inference from post-processing.

---

# 🟦 **4. Post-processing (C++ shared object)**

```bash
hailofilter function-name=yolov5 \
            so-path=.../libyolo_hailortpp_post.so \
            config-path=.../yolov5.json \
            qos=false !
```

This loads your **postprocess plugin written in C/C++**.

The `.so` takes the NN raw outputs (tensors) and turns them into:

* Bounding boxes
* Class IDs
* Confidences

and attaches them as **structured Hailo metadata**.

`config-path=yolov5.json` describes tensor shapes / anchors / strides etc.

➡️ You now have **meaningful detection objects per frame**.

---

### Queue #5

Ensures stable flow before overlay.

---

# 🟦 **5. Overlay (draw bounding boxes)**

```bash
hailooverlay qos=false !
```

Uses the metadata added by `hailofilter` and draws:

* bounding boxes
* labels
* confidence values
* shapes (if pose model)

Overlay works only because metadata is inside buffer.

➡️ You now have **annotated frames** ready to encode.

---

### Queue #6

```bash
queue leaky=no max-size-buffers=30 ...
```

Last decoupling before encoding.

---

# 🟦 **6. Convert to encoder-friendly format**

```bash
videoconvert n-threads=2 qos=false !
```

Encoders typically want I420 or NV12.
Overlay usually outputs ARGB or RGB.

➡️ This makes sure the frame is encoder-compatible.

---

# 🟦 **7. Encode to H.264**

```bash
x264enc tune=zerolatency speed-preset=ultrafast bitrate=4000 key-int-max=30 !
```

This is a **real-time low-latency encoder**:

* `tune=zerolatency` → no B-frames, no latency pipeline
* `speed-preset=ultrafast` → fastest encoding at cost of compression quality
* `bitrate=4000` → ~4 Mbps
* `key-int-max=30` → one keyframe every 30 frames (for robustness in streaming)

➡️ Produces **H.264-encoded video**.

---

# 🟦 **8. RTP packetization**

```bash
rtph264pay config-interval=1 pt=96 !
```

Wraps H.264 stream into RTP packets.

* `config-interval=1` → periodically send SPS/PPS in-band
  (very important for UDP clients that join mid-stream)

➡️ You get **RTP/H264 packets** over UDP.

---

# 🟦 **9. Send to network (UDP sink)**

```bash
udpsink host=<IP> port=5000
```

This transmits the RTP packets to a remote machine.

* <IP> = destination IP
* port = 5000

Your Python version exposes these as parameters.

---

# 📌 Full Functional Flow

```
FILE → DECODER → SCALE → CONVERT → HAILO INFERENCE
     (yolo HEF) → POSTPROCESS (C++ .so)
     → OVERLAY → FORMAT CONVERT → H.264 ENCODE
     → RTP PACKETIZE → UDP STREAM OUT
```

---

# 📌 Why this pipe is structured like this

### ✔ Maximum performance

Queues isolate CPU from NPU from encoder.

### ✔ Rockchip-friendly

Decoding → scaling → converting all done via CPU-optimized GStreamer plugins.

### ✔ Hailo workflow

hailonet → hailofilter → hailooverlay is the standard triplet.

### ✔ Real-time streaming

x264enc (zerolatency) + RTP + UDP ensures almost-zero overhead.

---

