# send stream

###  h264 sender

```
python3 sendStream.py \
  --role sender \
  --codec h264 \
  --host 192.168.1.100 \
  --port 5000 \
  --device /dev/video0 \
  --width 1280 --height 720 --framerate 120

```

```
python3 sendStream.py \
  --receiver \
  --codec h264 \
  --port 5000
```

###  raw sender

```
python3 sendStream.py \
  --role sender \
  --codec raw \
  --host 192.168.1.100 \
  --port 5000

```


```
python3 sendStream.py \
  --receiver \
  --codec raw \
  --port 5000 \
  --width 1280 --height 720
```