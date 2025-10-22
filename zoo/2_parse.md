# Parsing

pre-trained models are stored on AWS S3 and will be downloaded automatically when running the model zoo
into your data directory. 


### example

```
 hailomz parse yolox_tiny
PcieDevice scan_devices method is deprecated! Please use Device object.
[info] First time Hailo Dataflow Compiler is being used. Checking system requirements... (this might take a few seconds)
[Warning] It is recommended to have 32 GB of RAM, while this system has only 25 GB.
[Info] No GPU connected.
Component   Requirement      Found
==========  ==========       ==========  ==========
OS          Ubuntu           Ubuntu      Required
Release     20.04            20.04       Required
Package     python3-tk       V           Required
Package     graphviz         V           Required
Package     libgraphviz-dev  V           Required
Package     python3.8-dev    V           Required
RAM(GB)     16               25          Required
RAM(GB)     32               25          Recommended
CPU-Arch    x86_64           x86_64      Required
CPU-flag    avx              V           Required
Var:CC      unset            unset       Required
Var:CXX     unset            unset       Required
Var:LD      unset            unset       Required
Var:AS      unset            unset       Required
Var:AR      unset            unset       Required
Var:LN      unset            unset       Required
Var:DUMP    unset            unset       Required
Var:CPY     unset            unset       Required
In file included from /local/workspace/hailo_virtualenv/lib/python3.8/site-packages/numpy/core/include/numpy/ndarraytypes.h:1948,
                 from /local/workspace/hailo_virtualenv/lib/python3.8/site-packages/numpy/core/include/numpy/ndarrayobject.h:12,
                 from /local/workspace/hailo_virtualenv/lib/python3.8/site-packages/numpy/core/include/numpy/arrayobject.h:5,
                 from /home/hailo/.pyxbld/temp.linux-x86_64-3.8/pyrex/hailo_model_zoo/core/postprocessing/cython_utils/cython_nms.c:752:
/local/workspace/hailo_virtualenv/lib/python3.8/site-packages/numpy/core/include/numpy/npy_1_7_deprecated_api.h:17:2: warning: #warning "Using deprecated NumPy API, disable it with " "#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION" [-Wcpp]
   17 | #warning "Using deprecated NumPy API, disable it with " \
      |  ^~~~~~~
PcieDevice scan_devices method is deprecated! Please use Device object.
<Hailo Model Zoo INFO> Start run for network yolox_tiny ...
<Hailo Model Zoo INFO> Initializing the runner...
yolox_tiny.zip: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 17.9M/17.9M [00:29<00:00, 634kB/s]
[info] NMS structure of yolox (or equivalent architecture) was detected, a generated config file will be saved inside the har. To add NMS postprocessing to the model, please use the command: nms_postprocess(meta_arch=yolox).
[info] Translation completed on ONNX model yolox_tiny
[info] Initialized runner for yolox_tiny



du -h yolox_tiny.har
20M     yolox_tiny.har


```