# V4L get cemare data



```
[   74.128024] usb 1-1: new high-speed USB device number 2 using ehci-platform
[   74.276834] usb 1-1: New USB device found, idVendor=2560, idProduct=c154, bcdDevice= 0.00
[   74.276848] usb 1-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[   74.276857] usb 1-1: Product: See3CAM_CU55
[   74.276866] usb 1-1: Manufacturer: e-con systems
[   74.276874] usb 1-1: SerialNumber: 27225401
[   74.278451] uvcvideo: Found UVC 1.00 device See3CAM_CU55 (2560:c154)
[   74.309370] hid-generic 0003:2560:C154.0001: hiddev96,hidraw0: USB HID v1.11 Device [e-con systems See3CAM_CU55] on usb-fc800000.usb-1/input2



ls -l /dev/video*
crw-rw---- 1 root video 81, 0 Jun 26 02:47 /dev/video0
crw-rw---- 1 root video 81, 1 Jun 26 02:47 /dev/video1
```

```
v4l2-ctl -d /dev/video0 --list-formats-ext
ioctl: VIDIOC_ENUM_FMT
	Type: Video Capture

	[0]: 'UYVY' (UYVY 4:2:2)
		Size: Discrete 640x480
			Interval: Discrete 0.017s (60.000 fps)
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 1280x720
			Interval: Discrete 0.062s (16.000 fps)
			Interval: Discrete 0.125s (8.000 fps)
		Size: Discrete 1280x960
			Interval: Discrete 0.083s (12.000 fps)
			Interval: Discrete 0.167s (6.000 fps)
		Size: Discrete 1920x1080
			Interval: Discrete 0.125s (8.000 fps)
			Interval: Discrete 0.250s (4.000 fps)
		Size: Discrete 2560x1440
			Interval: Discrete 0.250s (4.000 fps)
			Interval: Discrete 0.500s (2.000 fps)
		Size: Discrete 2592x1944
			Interval: Discrete 0.333s (3.000 fps)
			Interval: Discrete 0.667s (1.500 fps)
	[1]: 'MJPG' (Motion-JPEG, compressed)
		Size: Discrete 640x480
			Interval: Discrete 0.017s (60.000 fps)
		Size: Discrete 1280x720
			Interval: Discrete 0.017s (60.000 fps)
		Size: Discrete 1280x960
			Interval: Discrete 0.017s (60.000 fps)
		Size: Discrete 1920x1080
			Interval: Discrete 0.017s (60.000 fps)
		Size: Discrete 2560x1440
			Interval: Discrete 0.017s (60.000 fps)
		Size: Discrete 2592x1944
			Interval: Discrete 0.017s (60.000 fps)
```

## test negotiate caps

```
gst-launch-1.0   v4l2src device=/dev/video0 !   video/x-raw,width=640,height=480,framerate=60/1 !   videoconvert !   fpsdisplaysink video-sink=fakesink text-overlay=false sync=false

```
