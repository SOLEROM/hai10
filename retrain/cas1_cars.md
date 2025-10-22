# retrain1

* get the model and do benchmarking

```

wget https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/HailoNets/LPR/vehicle_detector/yolov5m_vehicles/2022-08-25/yolov5m_vehicles.hef

(hailo_virtualenv) hailo@user-Latitude-5440: hailortcli benchmark yolov5m_vehicles.hef 
Starting Measurements...
Measuring FPS in HW-only mode
Network auto_group_0/yolov5m_vehicles: 100% | 1207 | FPS: 80.43 | ETA: 00:00:00
Measuring FPS (and Power on supported platforms) in streaming mode
[HailoRT] [warning] Using the overcurrent protection dvm for power measurement will disable the overcurrent protection.
If only taking one measurement, the protection will resume automatically.
If doing continuous measurement, to enable overcurrent protection again you have to stop the power measurement on this dvm.
Network auto_group_0/yolov5m_vehicles: 100% | 1205 | FPS: 80.30 | ETA: 00:00:00
Measuring HW Latency
Network auto_group_0/yolov5m_vehicles: 100% | 436 | HW Latency: 28.38 ms | ETA: 00:00:00

=======
Summary
=======
FPS     (hw_only)                 = 80.3676
        (streaming)               = 80.2997
Latency (hw)                      = 28.3828 ms
Device 0000:01:00.0:
  Power in streaming mode (average) = 2.79538 W
                          (max)     = 2.81937 W

```

## parse

```
> hailortcli parse-hef  yolov5m_vehicles.hef
Architecture HEF was compiled for: HAILO8
Network group name: auto_group_0, Single Context
    Network name: auto_group_0/yolov5m_vehicles
        VStream infos:
            Input  yolov5m_vehicles/input_layer1 UINT8, F8CR(1080x1920x3)
            Output yolov5m_vehicles/conv94 UINT8, NHWC(20x20x18)
            Output yolov5m_vehicles/conv85 UINT8, NHWC(40x40x18)
            Output yolov5m_vehicles/conv75 UINT8, NHWC(80x80x18)

```



## ? run infernece

```

toBin.py 
import cv2
import numpy as np

# Load the input image
image = cv2.imread('car1.jpg')

# Resize the image to 1920x1080
image = cv2.resize(image, (1920, 1080))

# Convert to RGB format if needed
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Normalize (if the model requires it) and convert to the correct data type
image = image / 255.0  # Normalize if the model expects values between 0 and 1
image = image.astype(np.float32)  # or np.uint8 if the model expects uint8

# Save to binary file
image.tofile('car1_input.bin')

```

```
> hailortcli run yolov5m_vehicles.hef --input-files car1_input.bin 
Running streaming inference (yolov5m_vehicles.hef):
  Transform data: true
    Type:      auto
    Quantized: true
Network auto_group_0/yolov5m_vehicles: 100% | 400 | FPS: 79.89 | ETA: 00:00:00
> Inference result:
 Network group: auto_group_0
    Frames count: 400
    FPS: 79.90
    Send Rate: 10603.48 Mbit/s
    Recv Rate: 96.65 Mbit/s



```

import hailo_platform.pyhailort as pyhailort

hef = pyhailort.pyhailort.HEF("yolov5m_vehicles.hef")
network_groups = hef.get_network_groups_infos()
    if len(network_groups) != 1:
        raise Exception("Expected a single network group in HEF")
network_group = network_groups[0]
    # Get input and output vstream infos
    input_vstream_infos = network_group.get_input_vstream_infos()
    output_vstream_infos = network_group.get_output_vstream_infos()