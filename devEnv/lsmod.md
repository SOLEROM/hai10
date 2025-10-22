

lsmod  | grep hailo
hailo_pci              94208  0


lspci  | grep Hailo
01:00.0 Co-processor: Hailo Technologies Ltd. Hailo-8 AI Processor (rev 01)


/sys/class/hailo_chardev/hailo0
├── board_location
├── dev
├── device_id
├── power
│   ├── async
│   ├── autosuspend_delay_ms
│   ├── control
│   ├── runtime_active_kids
│   ├── runtime_active_time
│   ├── runtime_enabled
│   ├── runtime_status
│   ├── runtime_suspended_time
│   └── runtime_usage
├── subsystem -> ../../../../class/hailo_chardev
└── uevent
