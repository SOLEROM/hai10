# missing hailo device

* accelerator_type was missing under /sys/class/hailo_chardev/hailo0

```

> hailortcli scan
[HailoRT] [error] CHECK failed - Failed open /sys/class/hailo_chardev/hailo0/accelerator_type
[HailoRT] [error] CHECK_SUCCESS failed with status=HAILO_DRIVER_FAIL(36)
[HailoRT] [error] CHECK_SUCCESS failed with status=HAILO_DRIVER_FAIL(36) - Failed parsing device info for hailo0
[HailoRT] [error] CHECK_SUCCESS failed with status=HAILO_DRIVER_FAIL(36)
[HailoRT] [error] CHECK_SUCCESS failed with status=HAILO_DRIVER_FAIL(36)
[HailoRT] [error] CHECK_SUCCESS failed with status=HAILO_DRIVER_FAIL(36)
[HailoRT] [error] CHECK_SUCCESS failed with status=HAILO_DRIVER_FAIL(36)
[HailoRT CLI] [error] CHECK_SUCCESS failed with status=HAILO_DRIVER_FAIL(36)
```

## issue1

* version mismatch between the driver and the CLI

```
> hailortcli --version
HailoRT-CLI version 4.18.0
>  dmesg | grep -i hailo | grep version
[    6.154859] hailo: Init module. driver version 4.17.0
```


upgrade to new install (pair2):

```
* hailo_ai_sw_suite_2024-10_docker
* hailort-pcie-driver_4.19.0_all.deb

both 4.19 issue fixed !!!!!!!!!


```