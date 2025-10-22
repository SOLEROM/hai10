# happy flow


## version

* must match
```
> hailortcli --version
HailoRT-CLI version 4.19.0
>  dmesg | grep -i hailo | grep version
[    6.154859] hailo: Init module. driver version 4.19.0
```


## scan

```
> hailortcli scan
Hailo Devices:
[-] Device: 0000:01:00.0


> (hailo_virtualenv) hailo -h
[info] First time Hailo Dataflow Compiler is being used. Checking system requirements... (this might take a few seconds)
[Info] No GPU connected.
[info] Current Time: 03:51:58, 11/06/24
[info] CPU: Architecture: x86_64, Model: 13th Gen Intel(R) Core(TM) i5-1345U, Number Of Cores: 12, Utilization: 0.0%
[info] Memory: Total: 15GB, Available: 13GB
[info] System info: OS: Linux, Kernel: 6.8.0-47-generic
[info] Hailo DFC Version: 3.29.0
[info] HailoRT Version: 4.19.0
[info] PCIe: 0000:01:00.0: Number Of Lanes: 2, Speed: 8.0 GT/s PCIe
````


## identify

```
> hailortcli fw-control identify

Executing on device: 0000:01:00.0
Identifying board
Control Protocol Version: 2
Firmware Version: 4.19.0 (release,app,extended context switch buffer)
Logger Version: 0
Board Name: Hailo-8
Device Architecture: HAILO8
Serial Number: yyyyyy
Part Number: xxxxx
Product Name: HAILO-8 AI ACCELERATOR M.2 B+M KEY MODULE



```

