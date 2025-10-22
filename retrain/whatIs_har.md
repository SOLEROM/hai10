# har tar


hailomz optimize convert from full precision into integer representation and generate a quantized Hailo Archive (HAR) file


The initial HAR file includes:

HN file, which is a JSON-like representation of the graph structure that is deployed to the Hailo hardware.
NPZ file, which includes the weights of the model.



### example


```
> tar xf yolov5m_vehicles.har


├── yolov5m_vehicles.hn
├── yolov5m_vehicles.nms.json
├── yolov5m_vehicles.npz
├── yolov5m_vehicles.original_model_meta.json
└── yolov5m_vehicles.postprocess.onnx
```