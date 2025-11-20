# hailort orig deb content

```
hailort_4.20.0_amd64.deb 
├── etc
│   └── default
│       └── hailort_service
├── lib
│   └── systemd
│       └── system
│           └── hailort.service
└── usr
    ├── bin
    │   └── hailortcli
    ├── include
    │   ├── gstreamer-1.0
    │   │   └── gst
    │   │       └── hailo
    │   │           ├── include
    │   │           │   └── hailo_gst.h
    │   │           └── tensor_meta.hpp
    │   └── hailo
    │       ├── buffer.hpp
    │       ├── device.hpp
    │       ├── dma_mapped_buffer.hpp
    │       ├── event.hpp
    │       ├── expected.hpp
    │       ├── genai
    │       │   ├── common.hpp
    │       │   ├── llm
    │       │   │   └── llm.hpp
    │       │   ├── text2image
    │       │   │   └── text2image.hpp
    │       │   └── vdevice_genai.hpp
    │       ├── hailort_common.hpp
    │       ├── hailort_defaults.hpp
    │       ├── hailort_dma-heap.h
    │       ├── hailort.h
    │       ├── hailort.hpp
    │       ├── hailo_session.hpp
    │       ├── hef.hpp
    │       ├── inference_pipeline.hpp
    │       ├── infer_model.hpp
    │       ├── network_group.hpp
    │       ├── network_rate_calculator.hpp
    │       ├── platform.h
    │       ├── quantization.hpp
    │       ├── runtime_statistics.hpp
    │       ├── stream.hpp
    │       ├── transform.hpp
    │       ├── vdevice.hpp
    │       └── vstream.hpp
    ├── lib
    │   ├── cmake
    │   │   └── HailoRT
    │   │       ├── HailoRTConfig.cmake
    │   │       ├── HailoRTConfigVersion.cmake
    │   │       ├── HailoRTTargets.cmake
    │   │       └── HailoRTTargets-release.cmake
    │   ├── libhailort.so.4.20.0
    │   └── x86_64-linux-gnu
    │       └── gstreamer-1.0
    │           └── libgsthailo.so
    ├── local
    │   └── bin
    │       └── hailort_service
    └── share
        └── doc
            └── hailort
                └── copyright

```