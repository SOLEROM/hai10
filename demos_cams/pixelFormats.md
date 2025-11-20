# pixel formats

## UYVY

```
UYVY (Uncompressed YUV 4:2:2)
Format: UYVY
Type: Raw, uncompressed video
Bandwidth: High
CPU load: Low
Latency: Very low
Quality: Perfect (no compression losses)
```

YUV 4:2:2 packed format:

```
U0 Y0 V0 Y1 U2 Y2 V2 Y3 ...

    Every 2 pixels share one U and one V component.

    Every pixel has its own Y (luma) value.

    This reduces color resolution a bit but keeps full brightness detail.
```

#### Cons

* Heavy on USB bandwidth:
```
        640×480 @ 60fps at UYVY:
        ~ 640×480×2 bytes × 60 ≈ ~36 MB/sec
```
* Cannot go to high resolutions without hitting USB 2 limits.
* make sure to use usb3


## MJPEG

* Motion JPEG

```
Format: MJPG
Type: Compressed video (each frame is a JPEG)
Bandwidth: Low
CPU load: Higher (needs JPEG decode)
Latency: Higher
Quality: Good, but lossy (compression artifacts may appear)
```

* Very small bandwidth:

```
    640×480 MJPEG @ 30–60fps ≈ 3–8 MB/sec
```


