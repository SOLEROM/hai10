# info

 print information of any network exists in the model zoo, to get a sense of its input/output shape,
parameters, operations, framework etc


```
hailomz info <model name>
```

## model names

```
> hailomz info --help


  model_name  Which network to run. Choices: arcface_mobilefacenet, arcface_mobilefacenet_nv12, arcface_mobilefacenet_rgbx, arcface_r50, centernet_resnet_v1_18_postprocess,
              centernet_resnet_v1_50_postprocess, centerpose_regnetx_1.6gf_fpn, centerpose_regnetx_800mf, centerpose_repvgg_a0, clip_resnet_50, damoyolo_tinynasL20_T,
              damoyolo_tinynasL25_S, damoyolo_tinynasL35_M, deeplab_v3_mobilenet_v2, deeplab_v3_mobilenet_v2_wo_dilation, detr_resnet_v1_18_bn, efficientdet_lite0,
              efficientdet_lite1, efficientdet_lite2, efficientnet_l, efficientnet_lite0, efficientnet_lite1, efficientnet_lite2, efficientnet_lite3, efficientnet_lite4,
              efficientnet_m, efficientnet_s, espcn_x2, espcn_x3, espcn_x4, face_attr_resnet_v1_18, face_attr_resnet_v1_18_nv12, face_attr_resnet_v1_18_rgbx, fast_depth,
              fast_depth_nv12_fhd, fcn16_resnet_v1_18, fcn8_resnet_v1_18, fcn8_resnet_v1_22, hand_landmark_lite, hardnet39ds, hardnet68, inception_v1, lightface_slim,
              lightface_slim_nv12, lightface_slim_nv12_fhd, lprnet, lprnet_yuy2, mobilenet_v1, mobilenet_v2_1.0, mobilenet_v2_1.4, mobilenet_v3,
              mobilenet_v3_large_minimalistic, mspn_regnetx_800mf, mspn_regnetx_800mf_nv12, nanodet_repvgg, nanodet_repvgg_a12, nanodet_repvgg_a1_640, osnet_x1_0,
              person_attr_resnet_v1_18, person_attr_resnet_v1_18_nv12, person_attr_resnet_v1_18_rgbx, regnetx_1.6gf, regnetx_800mf, regnety_200mf, repvgg_a0_person_reid_2048,
              repvgg_a0_person_reid_512, repvgg_a1, repvgg_a2, resmlp12_relu, resnet_v1_18, resnet_v1_34, resnet_v1_50, resnet_v2_18, resnet_v2_34, resnext26_32x4d,
              resnext50_32x4d, retinaface_mobilenet_v1, retinaface_mobilenet_v1_rgbx, scrfd_10g, scrfd_10g_nv12_fhd, scrfd_2.5g, scrfd_500m, shufflenet_g8_w1,
              squeezenet_v1.1, ssd_mobilenet_v1, ssd_mobilenet_v1_hd, ssd_mobilenet_v1_no_alls, ssd_mobilenet_v1_visdrone, ssd_mobilenet_v2, stdc1, tddfa_mobilenet_v1,
              tddfa_mobilenet_v1_nv12, tiny_yolov3, tiny_yolov4, tiny_yolov4_license_plates, tiny_yolov4_license_plates_yuy2, unet_mobilenet_v2, vit_base, vit_small,
              vit_tiny, yolact_mobilenet_v1, yolact_regnetx_1.6gf, yolact_regnetx_600mf_d2s_31classes, yolact_regnetx_800mf, yolact_regnetx_800mf_20classes, yolov3,
              yolov3_416, yolov3_gluon, yolov3_gluon_416, yolov4_leaky, yolov5l, yolov5l_seg, yolov5m, yolov5m6_6.1, yolov5m_6.1, yolov5m_seg, yolov5m_vehicles,
              yolov5m_vehicles_nv12, yolov5m_vehicles_yuy2, yolov5m_wo_spp, yolov5m_wo_spp_60p, yolov5m_wo_spp_60p_nv12_fhd, yolov5m_wo_spp_yuy2, yolov5n6_6.1, yolov5n_seg,
              yolov5n_seg_nv12_fhd, yolov5s, yolov5s6_6.1, yolov5s_c3tr, yolov5s_personface, yolov5s_personface_nv12, yolov5s_personface_nv12_fhd, yolov5s_personface_rgbx,
              yolov5s_seg, yolov5xs_wo_spp, yolov5xs_wo_spp_nms_core, yolov6n, yolov6n_0.2.1, yolov7, yolov7_tiny, yolov7e6, yolov8l, yolov8l_seg, yolov8m, yolov8m_seg,
              yolov8n, yolov8n_seg, yolov8s, yolov8s_seg, yolov8x, yolov8x_seg, yolox_l_leaky, yolox_s_leaky, yolox_s_wide_leaky, yolox_tiny, zero_dce
```


### example

```
hailomz info yolox_tiny
PcieDevice scan_devices method is deprecated! Please use Device object.
<Hailo Model Zoo INFO> Start run for network yolox_tiny ...
<Hailo Model Zoo INFO> 
        task:                    object detection
        input_shape:             416x416x3
        output_shape:            52x52x4, 52x52x1, 52x52x80, 26x26x4, 26x26x1, 26x26x80, 13x13x4, 13x13x1, 13x13x80
        operations:              6.44G
        parameters:              5.05M
        framework:               pytorch
        training_data:           coco train2017
        validation_data:         coco val2017
        eval_metric:             mAP
        full_precision_result:   32.64
        source:                  https://github.com/Megvii-BaseDetection/YOLOX
        license_url:             https://www.apache.org/licenses/LICENSE-2.0

```

## add data

* https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/DATA.rst

```
python /local/workspace/hailo_model_zoo/hailo_model_zoo/datasets/create_coco_tfrecord.py val2017
python /local/workspace/hailo_model_zoo/hailo_model_zoo/datasets/create_coco_tfrecord.py calib2017

```