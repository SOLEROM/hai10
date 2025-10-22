# profile

* generate hailo profiler report

The report contains information about your model and expected performance on the Hailo hardware.

### example


```

hailomz profile yolox_tiny
PcieDevice scan_devices method is deprecated! Please use Device object.
PcieDevice scan_devices method is deprecated! Please use Device object.
<Hailo Model Zoo INFO> Start run for network yolox_tiny ...
<Hailo Model Zoo INFO> Initializing the hailo8 runner...
[info] NMS structure of yolox (or equivalent architecture) was detected, a generated config file will be saved inside the har. To add NMS postprocessing to the model, please use the command: nms_postprocess(meta_arch=yolox).
[info] Translation completed on ONNX model yolox_tiny
[info] Initialized runner for yolox_tiny
[warning] In some cases, the performance estimation on pre_placement profiling mode might not be accurate. Post_placement mode would yield the best performance estimation.
[warning] Reducing optimization level to 0 (the accuracy won't be optimized and compression won't be used) because there's no available GPU
[info] Starting Hailo context-partitioner flow
                                                                                 17% 
context_0: conv11, conv12, ew_add2, conv13, conv14, ew_add3, conv15                        




[info] Using Multi-context flow
[info] Resources optimization guidelines: Strategy -> GREEDY Objective -> MAX_FPS
[info] Resources optimization params: max_control_utilization=60%, max_compute_utilization=60%, max_memory_utilization (weights)=60%, max_input_aligner_utilization=60%, max_apu_utilization=60%
[info] Successful Context-Partition
[info] 
+------------------------------------------------------------------+-------------+-----------------------+-----------------------+----------------+
| Node                                                             | Subclusters | L3 Weight Memory Cuts | L3 Output Memory Cuts | L4 Memory Cuts |
+------------------------------------------------------------------+-------------+-----------------------+-----------------------+----------------+
| input_layer1                                                     | 0           | 0                     | 0                     | 0.500          |
| auto_reshape_from_input_layer1_to_space_to_depth1                | 0           | 0                     | 0                     | 1.000          |
| space_to_depth1                                                  | 1           | 0                     | 12                    | 0.000          |
| conv1_sd4                                                        | 3           | 3                     | 5                     | 0.000          |
| conv1_sd5                                                        | 3           | 3                     | 1                     | 0.000          |
| shortcut_from_space_to_depth1_to_conv1_sd0-3                     | 1           | 0                     | 4                     | 0.000          |
| conv1_sd0                                                        | 3           | 3                     | 2                     | 0.000          |
| conv1_sd1                                                        | 3           | 3                     | 2                     | 0.000          |
| conv1_sd2                                                        | 3           | 3                     | 2                     | 0.000          |
| conv1_sd3                                                        | 3           | 3                     | 2                     | 0.000          |
| concat_from_conv1_sd0-3_to_conv1_sdc                             | 1           | 0                     | 4                     | 0.000          |
| conv1_sdc                                                        | 1           | 0                     | 4                     | 0.000          |
| conv2_sd4                                                        | 6           | 6                     | 1                     | 0.000          |
| shortcut_from_conv1_to_conv2_sd0-3                               | 1           | 0                     | 12                    | 0.000          |
| conv2_sd0                                                        | 6           | 6                     | 2                     | 0.000          |
| conv2_sd1                                                        | 6           | 6                     | 2                     | 0.000          |
| conv2_sd2                                                        | 6           | 6                     | 2                     | 0.000          |
| conv2_sd3                                                        | 6           | 6                     | 2                     | 0.000          |
| concat_from_conv2_sd0-3_to_conv2_sdc                             | 1           | 0                     | 1                     | 0.000          |
| conv2_sdc                                                        | 1           | 0                     | 4                     | 0.000          |
| conv3                                                            | 2           | 1                     | 10                    | 0.000          |
| conv5                                                            | 1           | 1                     | 1                     | 0.000          |
| smuffers_shortcut_conv5_to_conv6                                 | 1           | 0                     | 2                     | 0.000          |
| conv6_sd0                                                        | 6           | 3                     | 1                     | 0.000          |
| conv6_sd1                                                        | 6           | 3                     | 1                     | 0.000          |
| conv6_sdc                                                        | 1           | 0                     | 1                     | 0.000          |
| ew_add1                                                          | 1           | 0                     | 1                     | 0.000          |
| conv4                                                            | 3           | 3                     | 1                     | 0.000          |
| concat1                                                          | 1           | 0                     | 1                     | 0.000          |
| conv7                                                            | 3           | 3                     | 8                     | 0.000          |
| conv8_sd0                                                        | 6           | 6                     | 1                     | 0.000          |
| conv8_sd1                                                        | 6           | 6                     | 1                     | 0.000          |
| conv8_sd2                                                        | 6           | 6                     | 1                     | 0.000          |
| conv8_sd3                                                        | 6           | 6                     | 1                     | 0.000          |
| conv8_sdc                                                        | 1           | 0                     | 2                     | 0.000          |
| conv10                                                           | 2           | 1                     | 7                     | 0.000          |
| conv11                                                           | 1           | 1                     | 2                     | 0.000          |
| conv12_d0                                                        | 6           | 3                     | 4                     | 0.000          |
| conv12_d1                                                        | 6           | 3                     | 4                     | 0.000          |
| conv12_dc                                                        | 1           | 0                     | 1                     | 0.000          |
| ew_add2                                                          | 1           | 0                     | 2                     | 0.000          |
| conv13                                                           | 1           | 1                     | 2                     | 0.000          |
| conv14_d0                                                        | 6           | 3                     | 4                     | 0.000          |
| conv14_d1                                                        | 6           | 3                     | 4                     | 0.000          |
| conv14_dc                                                        | 1           | 0                     | 1                     | 0.000          |
| ew_add3                                                          | 1           | 0                     | 2                     | 0.000          |
| conv15                                                           | 1           | 1                     | 2                     | 0.000          |
| conv16_d0                                                        | 6           | 3                     | 4                     | 0.000          |
| conv16_d1                                                        | 6           | 3                     | 4                     | 0.000          |
| conv16_dc                                                        | 1           | 0                     | 1                     | 0.000          |
| ew_add4                                                          | 1           | 0                     | 1                     | 0.000          |
| conv9                                                            | 2           | 1                     | 12                    | 0.000          |
| concat2                                                          | 1           | 0                     | 1                     | 0.000          |
| conv17                                                           | 3           | 3                     | 8                     | 0.000          |
| conv18_sd0                                                       | 8           | 8                     | 1                     | 0.000          |
| conv18_sd1                                                       | 8           | 8                     | 1                     | 0.000          |
| conv18_sdc                                                       | 1           | 0                     | 2                     | 0.000          |
| conv19                                                           | 2           | 1                     | 2                     | 0.000          |
| conv21                                                           | 1           | 1                     | 2                     | 0.000          |
| conv22_d0                                                        | 6           | 3                     | 1                     | 0.000          |
| conv22_d1                                                        | 6           | 3                     | 1                     | 0.000          |
| conv22_dc                                                        | 1           | 0                     | 1                     | 0.000          |
| ew_add5                                                          | 1           | 0                     | 2                     | 0.000          |
| conv23                                                           | 1           | 1                     | 2                     | 0.000          |
| conv24_d0                                                        | 6           | 3                     | 1                     | 0.000          |
| conv24_d1                                                        | 6           | 3                     | 1                     | 0.000          |
| conv24_dc                                                        | 1           | 0                     | 1                     | 0.000          |
| ew_add6                                                          | 1           | 0                     | 2                     | 0.000          |
| conv25                                                           | 1           | 1                     | 2                     | 0.000          |
| conv26_d0                                                        | 6           | 3                     | 1                     | 0.000          |
| conv26_d1                                                        | 6           | 3                     | 1                     | 0.000          |
| conv26_dc                                                        | 1           | 0                     | 1                     | 0.000          |
| ew_add7                                                          | 1           | 0                     | 1                     | 0.000          |
| conv20                                                           | 2           | 1                     | 1                     | 0.000          |
| concat3                                                          | 1           | 0                     | 1                     | 0.000          |
| conv27                                                           | 4           | 2                     | 1                     | 0.000          |
| context_0_to_context_1_2                                         | 0           | 0                     | 0                     | 0.500          |
| context_0_to_context_1_in_3                                      | 0           | 0                     | 0                     | 0.500          |
| conv28_d0                                                        | 8           | 16                    | 1                     | 0.000          |
| conv28_d1                                                        | 8           | 16                    | 1                     | 0.000          |
| conv28_dc                                                        | 1           | 0                     | 1                     | 0.000          |
| conv29                                                           | 3           | 3                     | 4                     | 0.000          |
| maxpool1_fs                                                      | 1           | 0                     | 2                     | 0.000          |
| maxpool1_d0                                                      | 1           | 0                     | 1                     | 0.000          |
| maxpool1_d1                                                      | 1           | 0                     | 1                     | 0.000          |
| maxpool1_dc                                                      | 1           | 0                     | 1                     | 0.000          |
| maxpool2_fs                                                      | 1           | 0                     | 3                     | 0.000          |
| maxpool2_d0                                                      | 1           | 0                     | 1                     | 0.000          |
| maxpool2_d1                                                      | 1           | 0                     | 1                     | 0.000          |
| maxpool2_d2                                                      | 1           | 0                     | 1                     | 0.000          |
| maxpool2_dc                                                      | 1           | 0                     | 1                     | 0.000          |
| maxpool3_fs                                                      | 1           | 0                     | 3                     | 0.000          |
| maxpool3_d4                                                      | 1           | 0                     | 1                     | 0.000          |
| maxpool3_d5                                                      | 1           | 0                     | 1                     | 0.000          |
| fs_from_maxpool3_fs_to_maxpool3_d0-3                             | 1           | 0                     | 4                     | 0.000          |
| maxpool3_d0                                                      | 1           | 0                     | 1                     | 0.000          |
| maxpool3_d1                                                      | 1           | 0                     | 1                     | 0.000          |
| maxpool3_d2                                                      | 1           | 0                     | 1                     | 0.000          |
| maxpool3_d3                                                      | 1           | 0                     | 1                     | 0.000          |
| concat_from_maxpool3_d0-3_to_maxpool3_dc                         | 1           | 0                     | 1                     | 0.000          |
| maxpool3_dc                                                      | 1           | 0                     | 1                     | 0.000          |
| concat4                                                          | 1           | 0                     | 1                     | 0.000          |
| conv30                                                           | 6           | 12                    | 2                     | 0.000          |
| conv31                                                           | 3           | 3                     | 1                     | 0.000          |
| conv33                                                           | 1           | 2                     | 1                     | 0.000          |
| conv34                                                           | 8           | 16                    | 1                     | 0.000          |
| conv32                                                           | 3           | 3                     | 1                     | 0.000          |
| concat5                                                          | 1           | 0                     | 1                     | 0.000          |
| conv35                                                           | 5           | 5                     | 1                     | 0.000          |
| conv36                                                           | 3           | 3                     | 2                     | 0.000          |
| resize1                                                          | 1           | 0                     | 1                     | 0.000          |
| context_1_to_context_2_6                                         | 0           | 0                     | 0                     | 0.500          |
| context_1_to_context_2_in_7                                      | 0           | 0                     | 0                     | 0.500          |
| context_0_to_context_1_in_5                                      | 0           | 0                     | 0                     | 0.500          |
| concat6                                                          | 1           | 0                     | 2                     | 0.000          |
| conv37                                                           | 3           | 3                     | 1                     | 0.000          |
| conv39                                                           | 1           | 1                     | 1                     | 0.000          |
| conv40                                                           | 8           | 4                     | 1                     | 0.000          |
| conv38                                                           | 3           | 3                     | 1                     | 0.000          |
| concat7                                                          | 1           | 0                     | 1                     | 0.000          |
| conv41                                                           | 3           | 3                     | 3                     | 0.000          |
| conv42                                                           | 2           | 1                     | 2                     | 0.000          |
| resize2                                                          | 1           | 0                     | 1                     | 0.000          |
| context_0_to_context_1_0                                         | 0           | 0                     | 0                     | 0.500          |
| context_0_to_context_1_in_1                                      | 0           | 0                     | 0                     | 0.500          |
| concat8                                                          | 1           | 0                     | 2                     | 0.000          |
| conv43                                                           | 3           | 3                     | 1                     | 0.000          |
| conv45                                                           | 1           | 1                     | 2                     | 0.000          |
| conv46_d0                                                        | 3           | 3                     | 1                     | 0.000          |
| conv46_d1                                                        | 3           | 3                     | 1                     | 0.000          |
| conv46_dc                                                        | 1           | 0                     | 1                     | 0.000          |
| conv44                                                           | 3           | 3                     | 1                     | 0.000          |
| concat9                                                          | 1           | 0                     | 1                     | 0.000          |
| conv47                                                           | 3           | 3                     | 3                     | 0.000          |
| conv48_sd0                                                       | 4           | 4                     | 1                     | 0.000          |
| conv48_sd1                                                       | 4           | 4                     | 1                     | 0.000          |
| conv48_sdc                                                       | 1           | 0                     | 1                     | 0.000          |
| concat10                                                         | 1           | 0                     | 2                     | 0.000          |
| conv57                                                           | 2           | 1                     | 1                     | 0.000          |
| context_1_to_context_2_8                                         | 0           | 0                     | 0                     | 0.500          |
| context_1_to_context_2_in_9                                      | 0           | 0                     | 0                     | 0.500          |
| conv59                                                           | 2           | 1                     | 2                     | 0.000          |
| conv60_d0                                                        | 6           | 3                     | 1                     | 0.000          |
| conv60_d1                                                        | 6           | 3                     | 1                     | 0.000          |
| conv60_dc                                                        | 1           | 0                     | 1                     | 0.000          |
| conv58                                                           | 2           | 1                     | 1                     | 0.000          |
| context_1_to_context_2_10                                        | 0           | 0                     | 0                     | 0.500          |
| context_1_to_context_2_in_11                                     | 0           | 0                     | 0                     | 0.500          |
| concat11                                                         | 1           | 0                     | 1                     | 0.000          |
| conv61                                                           | 4           | 4                     | 9                     | 0.000          |
| conv62_sd0                                                       | 6           | 12                    | 1                     | 0.000          |
| conv62_sd1                                                       | 6           | 12                    | 1                     | 0.000          |
| conv62_sdc                                                       | 1           | 0                     | 1                     | 0.000          |
| concat12                                                         | 1           | 0                     | 2                     | 0.000          |
| conv71                                                           | 3           | 3                     | 1                     | 0.000          |
| conv73                                                           | 1           | 2                     | 6                     | 0.000          |
| conv74_d0                                                        | 6           | 6                     | 1                     | 0.000          |
| conv74_d1                                                        | 6           | 6                     | 1                     | 0.000          |
| conv74_dc                                                        | 1           | 0                     | 1                     | 0.000          |
| conv72                                                           | 3           | 3                     | 1                     | 0.000          |
| concat13                                                         | 1           | 0                     | 1                     | 0.000          |
| conv75                                                           | 5           | 5                     | 1                     | 0.000          |
| conv76                                                           | 1           | 2                     | 2                     | 0.000          |
| conv77                                                           | 3           | 3                     | 1                     | 0.000          |
| conv79                                                           | 3           | 3                     | 1                     | 0.000          |
| conv81                                                           | 1           | 1                     | 1                     | 0.000          |
| auto_reshape_from_conv81_to_output_layer8                        | 0           | 0                     | 0                     | 1.000          |
| output_layer8                                                    | 0           | 0                     | 0                     | 0.500          |
| conv78                                                           | 3           | 3                     | 1                     | 0.000          |
| conv80                                                           | 3           | 3                     | 2                     | 0.000          |
| conv82                                                           | 1           | 1                     | 1                     | 0.000          |
| output_layer7                                                    | 0           | 0                     | 0                     | 0.500          |
| conv83                                                           | 1           | 1                     | 1                     | 0.000          |
| output_layer9                                                    | 0           | 0                     | 0                     | 0.500          |
| conv63                                                           | 3           | 3                     | 4                     | 0.000          |
| conv64_d0                                                        | 6           | 3                     | 1                     | 0.000          |
| conv64_d1                                                        | 6           | 3                     | 1                     | 0.000          |
| conv64_dc                                                        | 1           | 0                     | 2                     | 0.000          |
| conv66_d0                                                        | 6           | 3                     | 1                     | 0.000          |
| conv66_d1                                                        | 6           | 3                     | 1                     | 0.000          |
| conv66_dc                                                        | 1           | 0                     | 1                     | 0.000          |
| conv68                                                           | 1           | 1                     | 1                     | 0.000          |
| auto_reshape_from_conv68_to_output_layer5                        | 0           | 0                     | 0                     | 1.000          |
| output_layer5                                                    | 0           | 0                     | 0                     | 0.500          |
| conv65_d0                                                        | 6           | 3                     | 1                     | 0.000          |
| conv65_d1                                                        | 6           | 3                     | 1                     | 0.000          |
| conv65_dc                                                        | 1           | 0                     | 2                     | 0.000          |
| conv67_d0                                                        | 6           | 3                     | 1                     | 0.000          |
| conv67_d1                                                        | 6           | 3                     | 1                     | 0.000          |
| conv67_dc                                                        | 1           | 0                     | 2                     | 0.000          |
| conv69                                                           | 1           | 1                     | 1                     | 0.000          |
| auto_reshape_from_conv69_to_output_layer4                        | 0           | 0                     | 0                     | 1.000          |
| output_layer4                                                    | 0           | 0                     | 0                     | 0.500          |
| conv70                                                           | 1           | 1                     | 1                     | 0.000          |
| auto_reshape_from_conv70_to_output_layer6                        | 0           | 0                     | 0                     | 1.000          |
| output_layer6                                                    | 0           | 0                     | 0                     | 0.500          |
| conv49                                                           | 3           | 3                     | 2                     | 0.000          |
| smuffers_shortcut_conv49_to_conv50                               | 1           | 0                     | 4                     | 0.000          |
| conv50_sd0                                                       | 6           | 6                     | 1                     | 0.000          |
| conv50_sd1                                                       | 6           | 6                     | 1                     | 0.000          |
| conv50_sd2                                                       | 6           | 6                     | 1                     | 0.000          |
| conv50_sd3                                                       | 6           | 6                     | 1                     | 0.000          |
| conv50_sdc                                                       | 1           | 0                     | 1                     | 0.000          |
| context_1_to_context_2_12                                        | 0           | 0                     | 0                     | 0.500          |
| context_1_to_context_2_in_13                                     | 0           | 0                     | 0                     | 0.500          |
| smuffers_shortcut_conv50_to_conv52                               | 1           | 0                     | 4                     | 0.000          |
| conv52_sd4                                                       | 6           | 6                     | 1                     | 0.000          |
| conv52_sd5                                                       | 6           | 6                     | 1                     | 0.000          |
| conv52_sd6                                                       | 6           | 6                     | 2                     | 0.000          |
| shortcut_from_smuffers_shortcut_conv50_to_conv52_to_conv52_sd0-3 | 1           | 0                     | 4                     | 0.000          |
| conv52_sd0                                                       | 6           | 6                     | 1                     | 0.000          |
| conv52_sd1                                                       | 6           | 6                     | 1                     | 0.000          |
| conv52_sd2                                                       | 6           | 6                     | 1                     | 0.000          |
| conv52_sd3                                                       | 6           | 6                     | 1                     | 0.000          |
| concat_from_conv52_sd0-3_to_conv52_sdc                           | 1           | 0                     | 1                     | 0.000          |
| conv52_sdc                                                       | 1           | 0                     | 1                     | 0.000          |
| conv54                                                           | 4           | 4                     | 2                     | 0.000          |
| auto_reshape_from_conv54_to_output_layer2                        | 0           | 0                     | 0                     | 1.000          |
| output_layer2                                                    | 0           | 0                     | 0                     | 0.500          |
| smuffers_shortcut_conv49_to_conv51                               | 1           | 0                     | 4                     | 0.000          |
| conv51_sd0                                                       | 6           | 6                     | 1                     | 0.000          |
| conv51_sd1                                                       | 6           | 6                     | 1                     | 0.000          |
| conv51_sd2                                                       | 6           | 6                     | 1                     | 0.000          |
| conv51_sd3                                                       | 6           | 6                     | 1                     | 0.000          |
| conv51_sdc                                                       | 1           | 0                     | 1                     | 0.000          |
| context_1_to_context_2_14                                        | 0           | 0                     | 0                     | 0.500          |
| context_1_to_context_2_in_15                                     | 0           | 0                     | 0                     | 0.500          |
| smuffers_shortcut_conv51_to_conv53                               | 1           | 0                     | 4                     | 0.000          |
| conv53_sd4                                                       | 6           | 6                     | 1                     | 0.000          |
| conv53_sd5                                                       | 6           | 6                     | 1                     | 0.000          |
| conv53_sd6                                                       | 6           | 6                     | 2                     | 0.000          |
| shortcut_from_smuffers_shortcut_conv51_to_conv53_to_conv53_sd0-3 | 1           | 0                     | 4                     | 0.000          |
| conv53_sd0                                                       | 6           | 6                     | 1                     | 0.000          |
| conv53_sd1                                                       | 6           | 6                     | 1                     | 0.000          |
| conv53_sd2                                                       | 6           | 6                     | 1                     | 0.000          |
| conv53_sd3                                                       | 6           | 6                     | 1                     | 0.000          |
| concat_from_conv53_sd0-3_to_conv53_sdc                           | 1           | 0                     | 1                     | 0.000          |
| conv53_sdc                                                       | 1           | 0                     | 4                     | 0.000          |
| conv55                                                           | 1           | 1                     | 1                     | 0.000          |
| auto_reshape_from_conv55_to_output_layer1                        | 0           | 0                     | 0                     | 1.000          |
| output_layer1                                                    | 0           | 0                     | 0                     | 0.500          |
| conv56                                                           | 1           | 1                     | 1                     | 0.000          |
| auto_reshape_from_conv56_to_output_layer3                        | 0           | 0                     | 0                     | 1.000          |
| output_layer3                                                    | 0           | 0                     | 0                     | 0.500          |
+------------------------------------------------------------------+-------------+-----------------------+-----------------------+----------------+
TOTAL:  LCUs: 211 (164.844%), Subclusters: 643 (125.586%), Weight memory cuts:521 (50.8789%), L3 Output memory cuts: 399 (38.9648%), L3 total cuts: 920 (89.8438%), L4 memory cuts: 8 (28.5714%)
[error] Error has occured during the layer latency calculation
[warning] output_layers_order in net_params don't match actual output layers in HN.
[warning] Failed removing file network.pb
[warning] Failed removing file mapped_graph.pb
[info] 
Model Details
-------------------------------  ----------
Input Tensors Shapes             416x416x3
Operations per Input Tensor      6.41 GOPs
Operations per Input Tensor      3.22 GMACs
Raw Operations per Input Tensor  6.41 GOPs
Raw Operations per Input Tensor  3.22 GMACs
Model Parameters                 7.31 M
-------------------------------  ----------

Profiler Input Settings
-----------------  -----------------
Optimization Goal  Reach Highest FPS
Profiler Mode      Pre Placement
-----------------  -----------------

Performance Summary
-------------------------------  ---
Number of Devices                1
Number of Contexts               3
Throughput                       N/A
Latency                          N/A
Total NN Core Power Consumption  N/A
Operations per Second            N/A
Operations per Second            N/A
Raw Operations per Second        N/A
Raw Operations per Second        N/A
-------------------------------  ---
<Hailo Model Zoo INFO> Profiler report generated in yolox_tiny.html

```