# Optimize

 convert them from full precision into integer representation and generate a quantized Hailo
Archive (HAR) file:


### example

```
> hailomz optimize yolox_tiny



<Hailo Model Zoo INFO> Start run for network yolox_tiny ...
<Hailo Model Zoo INFO> Initializing the hailo8 runner...
[info] Translation started on ONNX model yolox_tiny
[info] Restored ONNX model yolox_tiny (completion time: 00:00:00.06)
[info] Extracted ONNXRuntime meta-data for Hailo model (completion time: 00:00:00.33)
[info] NMS structure of yolox (or equivalent architecture) was detected.
[info] In order to use HailoRT post-processing capabilities, these end node names should be used: Sigmoid_264 Conv_261 Sigmoid_263 Sigmoid_285 Conv_282 Sigmoid_284 Sigmoid_306 Conv_303 Sigmoid_305.
[info] Start nodes mapped from original model: 'images': 'yolox_tiny/input_layer1'.
[info] End nodes mapped from original model: 'Conv_261', 'Sigmoid_263', 'Sigmoid_264', 'Conv_282', 'Sigmoid_284', 'Sigmoid_285', 'Conv_303', 'Sigmoid_305', 'Sigmoid_306'.
[info] Translation completed on ONNX model yolox_tiny (completion time: 00:00:00.67)
[info] Saved HAR to: /local/shared_with_docker/test1_yolox/yolox_tiny.har
<Hailo Model Zoo INFO> Preparing calibration data...
[info] Loading model script commands to yolox_tiny from /local/workspace/hailo_model_zoo/hailo_model_zoo/cfg/alls/generic/yolox_tiny.alls
[info] Starting Model Optimization
[warning] Reducing optimization level to 0 (the accuracy won't be optimized and compression won't be used) because there's no available GPU
[warning] Running model optimization with zero level of optimization is not recommended for production use and might lead to suboptimal accuracy results
[info] Model received quantization params from the hn
[info] Starting Mixed Precision
[info] Mixed Precision is done (completion time is 00:00:00.33)
[info] LayerNorm Decomposition skipped
[info] Starting Statistics Collector
[info] Using dataset with 64 entries for calibration
Calibration: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 64/64 [00:18<00:00,  3.53entries/s]
[info] Statistics Collector is done (completion time is 00:00:19.07)
[info] Starting Fix zp_comp Encoding
[info] Fix zp_comp Encoding is done (completion time is 00:00:00.00)
[info] Matmul Equalization skipped


[info] Finetune encoding skipped
[info] Bias Correction skipped
[info] Adaround skipped
[info] Quantization-Aware Fine-Tuning skipped
[info] Layer Noise Analysis skipped
[info] Model Optimization is done
[info] Saved HAR to: /local/shared_with_docker/test1_yolox/yolox_tiny.har



```