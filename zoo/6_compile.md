


```
> hailomz compile yolox_tiny


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
Calibration: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 64/64 [00:18<00:00,  3.54entries/s]
[info] Statistics Collector is done (completion time is 00:00:18.99)
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
[info] Loading model script commands to yolox_tiny from /local/workspace/hailo_model_zoo/hailo_model_zoo/cfg/alls/generic/yolox_tiny.alls
[info] To achieve optimal performance, set the compiler_optimization_level to "max" by adding performance_param(compiler_optimization_level=max) to the model script. Note that this may increase compilation time.
[info] Loading network parameters
[info] Starting Hailo allocation and compilation flow
[info] Adding an output layer after conv55
[info] Adding an output layer after conv54
..
....
..........




[info] +-----------+---------------------+---------------------+--------------------+
[info] | Cluster   | Control Utilization | Compute Utilization | Memory Utilization |
[info] +-----------+---------------------+---------------------+--------------------+
[info] | cluster_0 | 68.8%               | 59.4%               | 35.9%              |
[info] | cluster_1 | 43.8%               | 45.3%               | 24.2%              |
[info] | cluster_2 | 62.5%               | 53.1%               | 32%                |
[info] | cluster_3 | 81.3%               | 76.6%               | 40.6%              |
[info] | cluster_4 | 50%                 | 51.6%               | 37.5%              |
[info] | cluster_5 | 6.3%                | 12.5%               | 4.7%               |
[info] | cluster_6 | 62.5%               | 67.2%               | 48.4%              |
[info] | cluster_7 | 100%                | 81.3%               | 44.5%              |
[info] +-----------+---------------------+---------------------+--------------------+
[info] | Total     | 59.4%               | 55.9%               | 33.5%              |
[info] +-----------+---------------------+---------------------+--------------------+
[info] Successful Mapping (allocation time: 4m 25s)
[info] Compiling context_0...
[info] Compiling context_1...
[info] Bandwidth of model inputs: 3.96094 Mbps, outputs: 2.30152 Mbps (for a single frame)
[info] Bandwidth of DDR buffers: 0.0 Mbps (for a single frame)
[info] Bandwidth of inter context tensors: 6.43652 Mbps (for a single frame)
[info] Building HEF...
[info] Successful Compilation (compilation time: 5s)
[info] Saved HAR to: /local/shared_with_docker/test1_yolox/yolox_tiny.har
<Hailo Model Zoo INFO> HEF file written to yolox_tiny.hef

```