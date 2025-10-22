# eval



```

> hailomz eval yolox_tiny --data-count 100



PcieDevice scan_devices method is deprecated! Please use Device object.
usage: hailomz [-h] {parse,optimize,compile,profile,eval,info} ...
hailomz: error: unrecognized arguments: --date-count 100
(hailo_virtualenv) hailo@vladis:/local/workspace$ hailomz eval yolox_tiny --data-count 100
PcieDevice scan_devices method is deprecated! Please use Device object.
PcieDevice scan_devices method is deprecated! Please use Device object.
<Hailo Model Zoo INFO> Start run for network yolox_tiny ...
<Hailo Model Zoo INFO> Initializing the runner...
<Hailo Model Zoo INFO> Chosen target is full_precision
[info] NMS structure of yolox (or equivalent architecture) was detected, a generated config file will be saved inside the har. To add NMS postprocessing to the model, please use the command: nms_postprocess(meta_arch=yolox).
[info] Translation completed on ONNX model yolox_tiny
[info] Initialized runner for yolox_tiny
[info] Loading model script to yolox_tiny from /local/workspace/hailo_model_zoo/hailo_model_zoo/cfg/alls/generic/yolox_tiny.alls
<Hailo Model Zoo INFO> Initializing the dataset ...
<Hailo Model Zoo INFO> Running inference...
Processed: 100images [00:38,  2.61images/s]
creating index...
index created!
Loading and preparing results...
Converting ndarray to lists...
(10000, 7)
0/10000
DONE (t=0.06s)
creating index...
index created!
Running per image evaluation...
Evaluate annotation type *bbox*
DONE (t=1.26s).
Accumulating evaluation results...
DONE (t=0.43s).
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.385
 Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.566
 Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.414
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.183
 Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.438
 Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.639
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.296
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.443
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.456
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.219
 Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.517
 Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.731
<Hailo Model Zoo INFO> Done 100 images AP=38.458 AP50=56.564

```

