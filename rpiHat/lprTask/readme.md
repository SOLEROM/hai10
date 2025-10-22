# lpr task

## resources

dev statation x86 tappas full pipe demo:
* https://github.com/hailo-ai/tappas/blob/master/apps/h8/gstreamer/general/license_plate_recognition/README.rst




### hailo lpr
* lpr model page https://github.com/hailo-ai/hailo_model_zoo/tree/master/hailo_models/license_plate_recognition
* retrain docker: https://github.com/hailo-ai/hailo_model_zoo/blob/master/hailo_models/license_plate_recognition/docs/TRAINING_GUIDE.rst

### synthetic data
*  Hailo's LPRNet was trained on a synthetic auto-generated dataset containing 4 million license plate images. Auto-generation of synthetic data for training is cheap, allows one to obtain a large annotated dataset easily and can be adapted quickly for other domains
* https://github.com/hailo-ai/hailo_model_zoo/blob/master/hailo_models/license_plate_recognition/src/lp_autogenerate.ipynb