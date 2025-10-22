# 1 install


``` sudo apt install hailo-all```


## info

```
> apt show hailo-all
Package: hailo-all
Version: 4.18.0+1
Priority: optional
Section: video
Maintainer: Serge Schneider <serge@raspberrypi.com>
Installed-Size: 7168 B
Depends: hailofw (>= 4.18.0), hailort (>= 4.18.0), hailo-tappas-core (>= 3.29.1), rpicam-apps-hailo-postprocess (>= 1.5.1), python3-hailort (>= 4.18.0)
Breaks: hailo-dkms (<< 4.18.0)
Download-Size: 1186 B
APT-Manual-Installed: yes
APT-Sources: http://archive.raspberrypi.com/debian bookworm/main arm64 Packages
Description: Hailo support (metapackage)


```



## what inside:

```
> dpkg-query -L hailo-all
/.
/usr
/usr/share
/usr/share/doc
/usr/share/doc/hailo-all
/usr/share/doc/hailo-all/changelog.gz
```


## what depend

```
>apt-cache depends hailo-all
hailo-all
  Depends: hailofw
  Depends: hailort
  Depends: hailo-tappas-core
  Depends: rpicam-apps-hailo-postprocess
  Depends: python3-hailort
  Breaks: hailo-dkms


```

### deps content

```
dpkg-query -L hailofw
/.
/etc
/etc/modprobe.d
/etc/modprobe.d/hailo_pci.conf
/lib
/lib/firmware
/lib/firmware/hailo
/lib/firmware/hailo/hailo8_fw.4.17.0.bin
/lib/firmware/hailo/hailo8_fw.4.18.0.bin
/lib/udev
/lib/udev/rules.d
/lib/udev/rules.d/60-hailofw.rules
/usr
/usr/share
/usr/share/doc
/usr/share/doc/hailofw
/usr/share/doc/hailofw/changelog.Debian.gz


```

```
dpkg-query -L hailort
/.
/etc
/etc/default
/etc/default/hailort_service
/lib
/lib/systemd
/lib/systemd/system
/lib/systemd/system/hailort.service
/usr
/usr/bin
/usr/bin/hailortcli
/usr/include
/usr/include/gstreamer-1.0
/usr/include/gstreamer-1.0/gst
/usr/include/gstreamer-1.0/gst/hailo
/usr/include/gstreamer-1.0/gst/hailo/tensor_meta.hpp
/usr/include/hailo
/usr/include/hailo/buffer.hpp
/usr/include/hailo/device.hpp
/usr/include/hailo/dma_mapped_buffer.hpp
/usr/include/hailo/event.hpp
/usr/include/hailo/expected.hpp
/usr/include/hailo/hailort.h
/usr/include/hailo/hailort.hpp
/usr/include/hailo/hailort_common.hpp
/usr/include/hailo/hailort_defaults.hpp
/usr/include/hailo/hailort_dma-heap.h
/usr/include/hailo/hef.hpp
/usr/include/hailo/infer_model.hpp
/usr/include/hailo/inference_pipeline.hpp
/usr/include/hailo/network_group.hpp
/usr/include/hailo/network_rate_calculator.hpp
/usr/include/hailo/platform.h
/usr/include/hailo/quantization.hpp
/usr/include/hailo/runtime_statistics.hpp
/usr/include/hailo/stream.hpp
/usr/include/hailo/transform.hpp
/usr/include/hailo/vdevice.hpp
/usr/include/hailo/vstream.hpp
/usr/lib
/usr/lib/cmake
/usr/lib/cmake/HailoRT
/usr/lib/cmake/HailoRT/HailoRTConfig.cmake
/usr/lib/cmake/HailoRT/HailoRTConfigVersion.cmake
/usr/lib/cmake/HailoRT/HailoRTTargets-release.cmake
/usr/lib/cmake/HailoRT/HailoRTTargets.cmake
/usr/lib/libhailort.so.4.18.0
/usr/local
/usr/local/bin
/usr/local/bin/hailort_service
/usr/share
/usr/share/doc
/usr/share/doc/hailort
/usr/share/doc/hailort/copyright


```



```
dpkg-query -L hailo-tappas-core
/.
/etc
/etc/ld.so.preload.d
/etc/ld.so.preload.d/hailo_so.conf
/usr
/usr/include
/usr/include/hailo
/usr/include/hailo/tappas


....
..............


```


```
/.
/usr
/usr/lib
/usr/lib/aarch64-linux-gnu
/usr/lib/aarch64-linux-gnu/rpicam-apps-postproc
/usr/lib/aarch64-linux-gnu/rpicam-apps-postproc/hailo-postproc.so
/usr/share
/usr/share/doc
/usr/share/doc/rpicam-apps-hailo-postprocess
/usr/share/doc/rpicam-apps-hailo-postprocess/changelog.Debian.gz
/usr/share/doc/rpicam-apps-hailo-postprocess/copyright
/usr/share/hailo-models
/usr/share/hailo-models/resnet_v1_50_h8l.hef
/usr/share/hailo-models/yolov5_personface.json
/usr/share/hailo-models/yolov5n_seg_h8l_mz.hef
/usr/share/hailo-models/yolov5s_personface_h8l.hef
/usr/share/hailo-models/yolov5seg.json
/usr/share/hailo-models/yolov6n.hef
/usr/share/hailo-models/yolov8s_h8l.hef
/usr/share/hailo-models/yolov8s_pose_h8l_pi.hef
/usr/share/hailo-models/yolox_s_leaky_h8l_mz.hef
/usr/share/rpi-camera-assets
/usr/share/rpi-camera-assets/hailo_classifier.json
/usr/share/rpi-camera-assets/hailo_yolov5_personface.json
/usr/share/rpi-camera-assets/hailo_yolov5_segmentation.json
/usr/share/rpi-camera-assets/hailo_yolov6_inference.json
/usr/share/rpi-camera-assets/hailo_yolov8_inference.json
/usr/share/rpi-camera-assets/hailo_yolov8_pose.json
/usr/share/rpi-camera-assets/hailo_yolox_inference.json


```


```
dpkg-query -L python3-hailort              
/.
/usr
/usr/bin
/usr/bin/hailo
/usr/lib
/usr/lib/python3
/usr/lib/python3/dist-packages
/usr/lib/python3/dist-packages/hailo_platform
/usr/lib/python3/dist-packages/hailo_platform/__init__.py
/usr/lib/python3/dist-packages/hailo_platform/common
/usr/lib/python3/dist-packages/hailo_platform/common/__init__.py
/usr/lib/python3/dist-packages/hailo_platform/common/logger
/usr/lib/python3/dist-packages/hailo_platform/common/logger/__init__.py
/usr/lib/python3/dist-packages/hailo_platform/common/logger/logger.py
/usr/lib/python3/dist-packages/hailo_platform/drivers
/usr/lib/python3/dist-packages/hailo_platform/drivers/__init__.py
/usr/lib/python3/dist-packages/hailo_platform/drivers/control_object.py
/usr/lib/python3/dist-packages/hailo_platform/drivers/ethernet_utils.py
/usr/lib/python3/dist-packages/hailo_platform/drivers/hailo_controller
/usr/lib/python3/dist-packages/hailo_platform/drivers/hailo_controller/__init__.py
/usr/lib/python3/dist-packages/hailo_platform/drivers/hailo_controller/hailo_control_protocol.py
/usr/lib/python3/dist-packages/hailo_platform/drivers/hailo_controller/i2c_slaves.py
/usr/lib/python3/dist-packages/hailo_platform/drivers/hailo_controller/power_measurement.py
/usr/lib/python3/dist-packages/hailo_platform/drivers/hailort
/usr/lib/python3/dist-packages/hailo_platform/drivers/hailort/__init__.py
/usr/lib/python3/dist-packages/hailo_platform/drivers/hailort/pyhailort.py
/usr/lib/python3/dist-packages/hailo_platform/drivers/hw_object.py
/usr/lib/python3/dist-packages/hailo_platform/pyhailort
/usr/lib/python3/dist-packages/hailo_platform/pyhailort/__init__.py
/usr/lib/python3/dist-packages/hailo_platform/pyhailort/_pyhailort.cpython-311-aarch64-linux-gnu.so
/usr/lib/python3/dist-packages/hailo_platform/pyhailort/control_object.py
/usr/lib/python3/dist-packages/hailo_platform/pyhailort/ethernet_utils.py
/usr/lib/python3/dist-packages/hailo_platform/pyhailort/hailo_control_protocol.py
/usr/lib/python3/dist-packages/hailo_platform/pyhailort/hw_object.py
/usr/lib/python3/dist-packages/hailo_platform/pyhailort/i2c_slaves.py
/usr/lib/python3/dist-packages/hailo_platform/pyhailort/power_measurement.py
/usr/lib/python3/dist-packages/hailo_platform/pyhailort/pyhailort.py
/usr/lib/python3/dist-packages/hailo_platform/tools
/usr/lib/python3/dist-packages/hailo_platform/tools/__init__.py
/usr/lib/python3/dist-packages/hailo_platform/tools/hailocli
/usr/lib/python3/dist-packages/hailo_platform/tools/hailocli/__init__.py
/usr/lib/python3/dist-packages/hailo_platform/tools/hailocli/base_utils.py
/usr/lib/python3/dist-packages/hailo_platform/tools/hailocli/hailo_device_utils.py
/usr/lib/python3/dist-packages/hailo_platform/tools/hailocli/hailocli_commands.py
/usr/lib/python3/dist-packages/hailo_platform/tools/hailocli/main.py
/usr/lib/python3/dist-packages/hailo_platform/tools/hailocli/version_action.py
/usr/lib/python3/dist-packages/hailo_platform/tools/udp_rate_limiter.py
/usr/lib/python3/dist-packages/hailo_tutorials
/usr/lib/python3/dist-packages/hailo_tutorials/notebooks
/usr/lib/python3/dist-packages/hailo_tutorials/notebooks/HRT_0_Inference_Tutorial.ipynb
/usr/lib/python3/dist-packages/hailo_tutorials/notebooks/HRT_1_Power_Measurement_Tutorial.ipynb
/usr/lib/python3/dist-packages/hailo_tutorials/notebooks/HRT_2_Inference_Tutorial_Multi_Process_Service.ipynb
/usr/lib/python3/dist-packages/hailo_tutorials/notebooks/HRT_3_Inference_Single_Model_Tutorial.ipynb
/usr/lib/python3/dist-packages/hailo_tutorials/notebooks/HRT_4_Async_Inference_Multiple_Models_Tutorial.ipynb
/usr/lib/python3/dist-packages/hailort-4.18.0.egg-info
/usr/lib/python3/dist-packages/hailort-4.18.0.egg-info/PKG-INFO
/usr/lib/python3/dist-packages/hailort-4.18.0.egg-info/dependency_links.txt
/usr/lib/python3/dist-packages/hailort-4.18.0.egg-info/entry_points.txt
/usr/lib/python3/dist-packages/hailort-4.18.0.egg-info/not-zip-safe
/usr/lib/python3/dist-packages/hailort-4.18.0.egg-info/requires.txt
/usr/lib/python3/dist-packages/hailort-4.18.0.egg-info/top_level.txt
/usr/share
/usr/share/doc
/usr/share/doc/python3-hailort
/usr/share/doc/python3-hailort/changelog.Debian.gz
/usr/share/doc/python3-hailort/copyright
/usr/share/lintian
/usr/share/lintian/overrides
/usr/share/lintian/overrides/python3-hailort


```
