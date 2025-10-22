# unet_mobilenet_v2


```
python /local/workspace/hailo_model_zoo/hailo_model_zoo/datasets/create_oxford_pet_tfrecord.py  val

python /local/workspace/hailo_model_zoo/hailo_model_zoo/datasets/create_oxford_pet_tfrecord.py  calib
```


```
> hailomz info unet_mobilenet_v2
====================================
PcieDevice scan_devices method is deprecated! Please use Device object.
<Hailo Model Zoo INFO> Start run for network unet_mobilenet_v2 ...
<Hailo Model Zoo INFO> 
        task:                    semantic segmentation
        input_shape:             256x256x3
        output_shape:            256x256x3
        operations:              28.88G
        parameters:              10.08M
        framework:               TF2
        training_data:           oxford-IIIT pets
        validation_data:         oxford-IIIT pets
        eval_metric:             mIoU
        full_precision_result:   77.32
        source:                  https://www.tensorflow.org/tutorials/images/segmentation
        license_url:             https://www.apache.org/licenses/LICENSE-2.0
```

```
> hailomz parse unet_mobilenet_v2
====================================
-rw-rw-rw- 1 hailo ht        0 Jul  7 16:19 acceleras.log
-rw-rw-rw- 1 hailo ht      179 Jul  7 16:19 hailo_examples.log
-rw-rw-rw- 1 hailo ht        0 Jul  7 16:19 hailort.log
-rw-rw-rw- 1 hailo ht      219 Jul  7 16:19 hailo_sdk.client.log
-rw-rw-rw- 1 hailo ht      254 Jul  7 16:19 pyhailort.log
-rw-rw-rw- 1 hailo ht 40970240 Jul  7 16:19 unet_mobilenet_v2.har

```

```
hailomz profile unet_mobilenet_v2
====================================
<Hailo Model Zoo INFO> Start run for network unet_mobilenet_v2 ...
<Hailo Model Zoo INFO> Initializing the hailo8 runner...
[info] Translation completed on TensorFlow 2.x model unet_mobilenet_v2
[info] Initialized runner for unet_mobilenet_v2
[warning] In some cases, the performance estimation on pre_placement profiling mode might not be accurate. Post_placement mode would yield the best performance estimation.
[warning] Reducing optimization level to 0 (the accuracy won't be optimized and compression won't be used) because there's no available GPU
[info] Starting Hailo context-partitioner flow
[info] Using Single-context flow
[info] Resources optimization guidelines: Strategy -> GREEDY Objective -> MAX_FPS
[info] Resources optimization params: max_control_utilization=75%, max_compute_utilization=75%, max_memory_utilization (weights)=75%, max_input_aligner_utilization=75%, max_apu_utilization=75%
[info] Using Single-context flow
[info] Resources optimization guidelines: Strategy -> GREEDY Objective -> MAX_FPS
[info] Resources optimization params: max_control_utilization=75%, max_compute_utilization=75%, max_memory_utilization (weights)=75%, max_input_aligner_utilization=75%, max_apu_utilization=75%
[info] Successful Context-Partition
[info] 
+----------------------------------------------------------------------------------------------------------------------+-------------+-----------------------+-----------------------+----------------+
| Node                                                                                                                 | Subclusters | L3 Weight Memory Cuts | L3 Output Memory Cuts | L4 Memory Cuts |
+----------------------------------------------------------------------------------------------------------------------+-------------+-----------------------+-----------------------+----------------+
| input_layer1                                                                                                         | 0           | 0                     | 0                     | 0.500          |
| auto_reshape_from_input_layer1_to_conv1                                                                              | 0           | 0                     | 0                     | 1.000          |
| conv1                                                                                                                | 1           | 0                     | 1                     | 0.000          |
| dw1                                                                                                                  | 2           | 0                     | 1                     | 0.000          |
| conv2                                                                                                                | 1           | 0                     | 1                     | 0.000          |
| conv3                                                                                                                | 1           | 0                     | 9                     | 0.000          |
| dw2                                                                                                                  | 1           | 0                     | 1                     | 0.000          |
| conv4                                                                                                                | 1           | 0                     | 2                     | 0.000          |
| conv5                                                                                                                | 1           | 0                     | 1                     | 0.000          |
| dw3_lanes_feature_splitter                                                                                           | 1           | 0                     | 2                     | 0.000          |
| dw3_lanes_2                                                                                                          | 2           | 0                     | 2                     | 0.000          |
| dw3_lanes_concat                                                                                                     | 1           | 0                     | 1                     | 0.000          |
| conv6                                                                                                                | 1           | 0                     | 1                     | 0.000          |
| conv7                                                                                                                | 1           | 0                     | 3                     | 0.000          |
| dw4                                                                                                                  | 1           | 0                     | 1                     | 0.000          |
| conv8                                                                                                                | 1           | 0                     | 2                     | 0.000          |
| conv9                                                                                                                | 1           | 0                     | 1                     | 0.000          |
| dw5                                                                                                                  | 1           | 0                     | 1                     | 0.000          |
| conv10                                                                                                               | 1           | 0                     | 2                     | 0.000          |
| conv11                                                                                                               | 1           | 0                     | 1                     | 0.000          |
| dw6                                                                                                                  | 1           | 0                     | 1                     | 0.000          |
| conv12                                                                                                               | 1           | 0                     | 1                     | 0.000          |
| conv13                                                                                                               | 1           | 0                     | 14                    | 0.000          |
| dw7                                                                                                                  | 1           | 0                     | 1                     | 0.000          |
| conv14                                                                                                               | 1           | 0                     | 2                     | 0.000          |
| conv15                                                                                                               | 2           | 0                     | 1                     | 0.000          |
| dw8                                                                                                                  | 1           | 0                     | 1                     | 0.000          |
| conv16                                                                                                               | 2           | 0                     | 2                     | 0.000          |
| conv17                                                                                                               | 2           | 0                     | 1                     | 0.000          |
| dw9                                                                                                                  | 1           | 0                     | 1                     | 0.000          |
| conv18                                                                                                               | 2           | 0                     | 2                     | 0.000          |
| conv19                                                                                                               | 2           | 0                     | 1                     | 0.000          |
| dw10                                                                                                                 | 1           | 0                     | 1                     | 0.000          |
| conv20                                                                                                               | 2           | 0                     | 1                     | 0.000          |
| conv21                                                                                                               | 2           | 0                     | 1                     | 0.000          |
| dw11                                                                                                                 | 1           | 0                     | 1                     | 0.000          |
| conv22                                                                                                               | 3           | 0                     | 2                     | 0.000          |
| conv23                                                                                                               | 4           | 0                     | 2                     | 0.000          |
| dw12                                                                                                                 | 1           | 0                     | 1                     | 0.000          |
| conv24                                                                                                               | 4           | 0                     | 2                     | 0.000          |
| conv25                                                                                                               | 4           | 0                     | 2                     | 0.000          |
| dw13                                                                                                                 | 1           | 0                     | 2                     | 0.000          |
| conv26                                                                                                               | 4           | 0                     | 1                     | 0.000          |
| conv27                                                                                                               | 4           | 0                     | 8                     | 0.000          |
| dw14                                                                                                                 | 1           | 0                     | 1                     | 0.000          |
| conv28                                                                                                               | 7           | 0                     | 2                     | 0.000          |
| conv29                                                                                                               | 4           | 4                     | 1                     | 0.000          |
| dw15                                                                                                                 | 4           | 0                     | 1                     | 0.000          |
| conv30                                                                                                               | 2           | 4                     | 2                     | 0.000          |
| conv31                                                                                                               | 4           | 4                     | 1                     | 0.000          |
| dw16                                                                                                                 | 4           | 0                     | 1                     | 0.000          |
| conv32                                                                                                               | 2           | 4                     | 1                     | 0.000          |
| conv33                                                                                                               | 4           | 4                     | 1                     | 0.000          |
| dw17                                                                                                                 | 4           | 0                     | 1                     | 0.000          |
| conv34                                                                                                               | 7           | 7                     | 2                     | 0.000          |
| deconv1_defuse_conv_d0                                                                                               | 4           | 40                    | 1                     | 0.000          |
| deconv1_defuse_conv_d1                                                                                               | 4           | 40                    | 1                     | 0.000          |
| deconv1_defuse_conv_dc                                                                                               | 1           | 0                     | 1                     | 0.000          |
| deconv1_defuse_fi0                                                                                                   | 1           | 0                     | 1                     | 0.000          |
| concat1                                                                                                              | 1           | 0                     | 3                     | 0.000          |
| deconv2_defuse_conv_d4                                                                                               | 8           | 24                    | 1                     | 0.000          |
| deconv2_defuse_conv_d5                                                                                               | 8           | 24                    | 1                     | 0.000          |
| shortcut_from_concat1_to_deconv2_defuse_conv_d0_deconv2_defuse_conv_d1_deconv2_defuse_conv_d2_deconv2_defuse_conv_d3 | 1           | 0                     | 2                     | 0.000          |
| deconv2_defuse_conv_d3                                                                                               | 8           | 24                    | 1                     | 0.000          |
| concat_from_deconv2_defuse_conv_d3_deconv2_defuse_conv_d4_to_concat_from_deconv2_defuse_conv_d3_deconv2_defus        | 1           | 0                     | 1                     | 0.000          |
| concat_from_deconv2_defuse_conv_d3_deconv2_defuse_conv_d4_deconv2_defuse_conv_d5_to_deconv2_defuse_conv_dc           | 1           | 0                     | 1                     | 0.000          |
| shortcut_from_shortcut_from_concat1_to_deconv2_defuse_conv_d0_deconv2_defuse_conv_d1_deconv2_defuse_conv_d2_d        | 1           | 0                     | 2                     | 0.000          |
| deconv2_defuse_conv_d2                                                                                               | 8           | 24                    | 1                     | 0.000          |
| shortcut_from_shortcut_from_shortcut_from_concat1_to_deconv2_defuse_conv_d0_deconv2_defuse_conv_d1_deconv2_de        | 1           | 0                     | 2                     | 0.000          |
| deconv2_defuse_conv_d0                                                                                               | 8           | 24                    | 1                     | 0.000          |
| deconv2_defuse_conv_d1                                                                                               | 8           | 24                    | 1                     | 0.000          |
| concat_from_deconv2_defuse_conv_d0_deconv2_defuse_conv_d1_to_concat_from_deconv2_defuse_conv_d0_deconv2_defus        | 1           | 0                     | 1                     | 0.000          |
| concat_from_deconv2_defuse_conv_d0_deconv2_defuse_conv_d1_deconv2_defuse_conv_d2_to_deconv2_defuse_conv_dc           | 1           | 0                     | 1                     | 0.000          |
| deconv2_defuse_conv_dc                                                                                               | 1           | 0                     | 2                     | 0.000          |
| deconv2_defuse_fi0                                                                                                   | 1           | 0                     | 1                     | 0.000          |
| concat2                                                                                                              | 1           | 0                     | 4                     | 0.000          |
| deconv3_defuse_conv_d0                                                                                               | 8           | 8                     | 1                     | 0.000          |
| deconv3_defuse_conv_d1                                                                                               | 8           | 8                     | 1                     | 0.000          |
| deconv3_defuse_conv_d2                                                                                               | 8           | 8                     | 1                     | 0.000          |
| concat_from_deconv3_defuse_conv_d0_deconv3_defuse_conv_d1_deconv3_defuse_conv_d2_to_deconv3_defuse_conv_dc           | 1           | 0                     | 1                     | 0.000          |
| deconv3_defuse_conv_d3                                                                                               | 8           | 8                     | 1                     | 0.000          |
| deconv3_defuse_conv_dc                                                                                               | 1           | 0                     | 1                     | 0.000          |
| deconv3_defuse_fi0                                                                                                   | 1           | 0                     | 1                     | 0.000          |
| l4_portal_from_conv7_to_concat3                                                                                      | 0           | 0                     | 0                     | 11.000         |
| concat3                                                                                                              | 1           | 0                     | 8                     | 0.000          |
| deconv4_defuse_conv_sd0                                                                                              | 8           | 8                     | 1                     | 0.000          |
| deconv4_defuse_conv_sd1                                                                                              | 8           | 8                     | 1                     | 0.000          |
| deconv4_defuse_conv_sd2                                                                                              | 8           | 8                     | 1                     | 0.000          |
| deconv4_defuse_conv_sd3                                                                                              | 8           | 8                     | 1                     | 0.000          |
| deconv4_defuse_conv_sdc                                                                                              | 1           | 0                     | 2                     | 0.000          |
| deconv4_defuse_fi0                                                                                                   | 1           | 0                     | 1                     | 0.000          |
| ddr_portal_from_conv3_to_concat4                                                                                     | 0           | 0                     | 0                     | 0.000          |
| concat4                                                                                                              | 1           | 0                     | 6                     | 0.000          |
| deconv5_defuse_conv_sd0                                                                                              | 2           | 0                     | 1                     | 0.000          |
| deconv5_defuse_conv_sd1                                                                                              | 2           | 0                     | 1                     | 0.000          |
| deconv5_defuse_conv_sd2                                                                                              | 2           | 0                     | 1                     | 0.000          |
| deconv5_defuse_conv_sdc                                                                                              | 1           | 0                     | 1                     | 0.000          |
| deconv5_defuse_fi0                                                                                                   | 1           | 0                     | 1                     | 0.000          |
| auto_reshape_from_deconv5_defuse_fi0_to_output_layer1                                                                | 0           | 0                     | 0                     | 1.000          |
| output_layer1                                                                                                        | 0           | 0                     | 0                     | 0.500          |
+----------------------------------------------------------------------------------------------------------------------+-------------+-----------------------+-----------------------+----------------+
TOTAL:  LCUs: 94 (73.4375%), Subclusters: 259 (50.5859%), Weight memory cuts:315 (30.7617%), L3 Output memory cuts: 162 (15.8203%), L3 total cuts: 477 (46.582%), L4 memory cuts: 13 (46.4286%)
[warning] Failed removing file network.pb
[warning] Failed removing file mapped_graph.pb
[info] 
Model Details
-------------------------------  -----------
Input Tensors Shapes             256x256x3
Operations per Input Tensor      8.34 GOPs
Operations per Input Tensor      4.18 GMACs
Raw Operations per Input Tensor  28.85 GOPs
Raw Operations per Input Tensor  14.44 GMACs
Model Parameters                 10.93 M
-------------------------------  -----------

Profiler Input Settings
-----------------  -----------------
Optimization Goal  Reach Highest FPS
Profiler Mode      Pre Placement
-----------------  -----------------

Performance Summary
-------------------------------  --------------
Number of Devices                1
Number of Contexts               1
Throughput                       433.38 FPS
Latency                          6.34 ms
Total NN Core Power Consumption  1.64 W
Operations per Second            3613.44 GOP/s
Operations per Second            1811.46 GMAC/s
Raw Operations per Second        12502.24 GOP/s
Raw Operations per Second        6255.80 GMAC/s
-------------------------------  --------------



-rw-rw-rw- 1 hailo ht        0 Jul  7 16:22 allocator.log
-rw-rw-rw- 1 hailo ht    33053 Jul  7 16:23 estimation.csv
-rw-rw-rw- 1 hailo ht   315918 Jul  7 16:23 hailo_sdk.core.log
-rw-rw-rw- 1 hailo ht  1642686 Jul  7 16:23 unet_mobilenet_v2.html

```


```
hailomz optimize unet_mobilenet_v2
====================================

hailomz optimize unet_mobilenet_v2 
PcieDevice scan_devices method is deprecated! Please use Device object.
PcieDevice scan_devices method is deprecated! Please use Device object.
<Hailo Model Zoo INFO> Start run for network unet_mobilenet_v2 ...
<Hailo Model Zoo INFO> Initializing the hailo8 runner...
[info] Translation completed on TensorFlow 2.x model unet_mobilenet_v2
[info] Initialized runner for unet_mobilenet_v2
<Hailo Model Zoo INFO> Preparing calibration data...
[info] Loading model script to unet_mobilenet_v2 from /local/workspace/hailo_model_zoo/hailo_model_zoo/cfg/alls/generic/unet_mobilenet_v2.alls
[info] Starting Model Optimization
[warning] Reducing optimization level to 0 (the accuracy won't be optimized and compression won't be used) because there's no available GPU
[info] Using dataset with 256 entries for calibration
[info] Starting Stats Collector
Calibration: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 256/256 [01:21<00:00,  3.12entries/s]
[info] Stats Collector is done (completion time is 00:01:22.50)
[info] No shifts available for layer unet_mobilenet_v2/deconv2/conv_op, using max shift instead. delta=0.3562470327566043
[info] No shifts available for layer unet_mobilenet_v2/deconv5/conv_op, using max shift instead. delta=0.15921388965605843
[info] Bias Correction skipped
[info] Adaround skipped
[info] Starting Fine Tune
Corrupt JPEG data: 240 extraneous bytes before marker 0xd9
Corrupt JPEG data: premature end of data segment
[warning] Dataset is larger than expected size. Increasing the algorithm dataset size might improve the results
[info] Using dataset with 2048 entries for finetune
Epoch 1/4
130/256 [==============>...............] - ETA: 12:10 - total_distill_loss: 0.4581 - _distill_loss_unet_mobilenet_v2/deconv5: 0.4581Corrupt JPEG data: 240 extraneous bytes before marker 0xd9


256/256 [==============================] - 1502s 6s/step - total_distill_loss: 0.2670 - _distill_loss_unet_mobilenet_v2/deconv5: 0.2670
[info] Fine Tune is done (completion time is 01:40:51.08)
[info] Layer Noise Analysis skipped
[info] Model Optimization is done


-rw-rw-rw- 1 hailo ht      2511 Jul  7 23:51 acceleras.log
-rw-rw-rw- 1 hailo ht         0 Jul  7 16:22 allocator.log
-rw-rw-rw- 1 hailo ht     33053 Jul  7 16:23 estimation.csv
-rw-rw-rw- 1 hailo ht      2485 Jul  7 22:08 hailo_examples.log
-rw-rw-rw- 1 hailo ht         0 Jul  7 16:19 hailort.log
-rw-rw-rw- 1 hailo ht      5573 Jul  7 23:51 hailo_sdk.client.log
-rw-rw-rw- 1 hailo ht    315918 Jul  7 16:23 hailo_sdk.core.log
-rw-rw-rw- 1 hailo ht      2032 Jul  7 22:08 pyhailort.log
drwxrwxrwx 2 hailo ht      4096 Jul  7 20:57 .stats_collection/
-rw-rw-rw- 1 hailo ht 181043200 Jul  7 23:51 unet_mobilenet_v2.har
-rw-rw-rw- 1 hailo ht   1642686 Jul  7 16:23 unet_mobilenet_v2.html


```

```
hailomz eval unet_mobilenet_v2
hailomz eval unet_mobilenet_v2 --target emulator


> hailomz eval unet_mobilenet_v2 --data-count 10

<Hailo Model Zoo INFO> Start run for network unet_mobilenet_v2 ...
<Hailo Model Zoo INFO> Initializing the runner...
<Hailo Model Zoo INFO> Chosen target is full_precision
[info] Translation completed on TensorFlow 2.x model unet_mobilenet_v2
[info] Initialized runner for unet_mobilenet_v2
[info] Loading model script to unet_mobilenet_v2 from /local/workspace/hailo_model_zoo/hailo_model_zoo/cfg/alls/generic/unet_mobilenet_v2.alls
<Hailo Model Zoo INFO> Initializing the dataset ...
<Hailo Model Zoo INFO> Running inference...
Processed: 10images [00:06,  1.53images/s]
<Hailo Model Zoo INFO> Done 10 images mIoU=78.040

```


```
hailomz eval unet_mobilenet_v2 --­­visualize

hailo_model_zoo.core.postprocessing.segmentation_postprocessing.PostProcessingException: Visualization is not implemented for dataset oxford_pet

```


```
-rw-rw-rw- 1 hailo ht 2.5K Jul  7 23:51 acceleras.log
-rw-rw-rw- 1 hailo ht    0 Jul  7 16:22 allocator.log
-rw-rw-rw- 1 hailo ht  33K Jul  7 16:23 estimation.csv
-rw-rw-rw- 1 hailo ht 3.8K Jul  8 08:12 hailo_examples.log
-rw-rw-rw- 1 hailo ht    0 Jul  7 16:19 hailort.log
-rw-rw-rw- 1 hailo ht 6.7K Jul  8 08:12 hailo_sdk.client.log
-rw-rw-rw- 1 hailo ht 309K Jul  7 16:23 hailo_sdk.core.log
-rw-rw-rw- 1 hailo ht 3.0K Jul  8 08:12 pyhailort.log
drwxrwxrwx 2 hailo ht 4.0K Jul  7 20:57 .stats_collection/
-rw-rw-rw- 1 hailo ht  40M Jul  8 08:12 unet_mobilenet_v2.har
-rw-rw-rw- 1 hailo ht 1.6M Jul  7 16:23 unet_mobilenet_v2.html

```