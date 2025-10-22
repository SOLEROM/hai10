# setting started

## intro
* https://www.youtube.com/watch?v=_aCyR8XJcws (gilad intro)

ref:

* https://github.com/hailo-ai/hailo-rpi5-examples
* https://github.com/hailo-ai/hailo_model_zoo


## pre
* update pi
* install sw
``` sudo apt install hailo-all ```
* pciE gen3:
``` sudo raspi-config ; 6 Advanced Options", then select option "A8 PCIe Speed".  ; reboot ```
* verify:
``` 
hailortcli fw-control identify 
gst-inspect-1.0 hailotools
gst-inspect-1.0 hailo

```

* exmaple code:

```
mkdir /proj ; sudo chmod 777 /proj ; cd /proj
git clone https://github.com/hailo-ai/hailo-rpi5-examples.git
```


```
cd hailo-rpi5-examples/
./install.sh

source  setup_env.sh 
pip install -r requirements.txt 
sudo apt install -y rapidjson-dev
./download_resources.sh --all
./compile_postprocess.sh

```



## cam source

```
python basic_pipelines/get_usb_camera.py

python basic_pipelines/detection.py --input /dev/video<X>

```

## examples:


