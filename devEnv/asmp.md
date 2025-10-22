


dmesg |grep hai
[    0.000000]   zhaoxin   Shanghai  
[    6.162994] hailo_pci: loading out-of-tree module taints kernel.
[    6.162999] hailo_pci: module verification failed: signature and/or required key missing - tainting kernel
[    6.163623] hailo: Init module. driver version 4.17.0
[    6.163651] hailo 0000:01:00.0: Probing on: 1e60:2864...
[    6.163654] hailo 0000:01:00.0: Probing: Allocate memory for device extension, 11600
[    6.163660] hailo 0000:01:00.0: enabling device (0000 -> 0002)
[    6.164051] hailo 0000:01:00.0: Probing: Device enabled
[    6.164069] hailo 0000:01:00.0: Probing: mapped bar 0 - 00000000f5b4cfde 16384
[    6.164075] hailo 0000:01:00.0: Probing: mapped bar 2 - 00000000d6e795ed 4096
[    6.164079] hailo 0000:01:00.0: Probing: mapped bar 4 - 00000000627c9a54 16384
[    6.164082] hailo 0000:01:00.0: Probing: Setting max_desc_page_size to 4096, (page_size=4096)
[    6.164135] hailo 0000:01:00.0: Probing: Enabled 64 bit dma
[    6.164136] hailo 0000:01:00.0: Probing: Using specialized dma_ops=iommu_dma_ops
[    6.164142] hailo 0000:01:00.0: Probing: Using userspace allocated vdma buffers
[    6.164145] hailo 0000:01:00.0: Disabling ASPM L0s 


[    6.164146] hailo 0000:01:00.0: can't disable ASPM; OS doesn't have ASPM control


[    6.164147] hailo 0000:01:00.0: Successfully disabled ASPM L0s 
[    6.298571] hailo 0000:01:00.0: Firmware was loaded successfully
[    6.312992] hailo 0000:01:00.0: Probing: Added board 1e60-2864, /dev/hailo0





ASPM is a power-saving feature for PCI Express devices that reduces power consumption by putting links into a low-power state when idle.

Some BIOS/UEFI firmware versions do not allow the operating system to override ASPM settings, leading to these kernel messages.

## fix1?

before /proc/cmdline 
BOOT_IMAGE=/boot/vmlinuz-6.8.0-47-generic root=UUID=292f246a-8cb1-4954-86f1-302e49c03fb1 ro quiet splash vt.handoff=7

/etc/default/grub
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash pcie_aspm=force"
sudo update-grub



> cat /proc/cmdline 
BOOT_IMAGE=/boot/vmlinuz-6.8.0-47-generic root=UUID=292f246a-8cb1-4954-86f1-302e49c03fb1 ro quiet splash pcie_aspm=force vt.handoff=7

> dmesg | grep -i hailo
[    6.202440] hailo_pci: loading out-of-tree module taints kernel.
[    6.202445] hailo_pci: module verification failed: signature and/or required key missing - tainting kernel
[    6.203389] hailo: Init module. driver version 4.17.0
[    6.203794] hailo 0000:01:00.0: Probing on: 1e60:2864...
[    6.203798] hailo 0000:01:00.0: Probing: Allocate memory for device extension, 11600
[    6.203806] hailo 0000:01:00.0: enabling device (0000 -> 0002)
[    6.203870] hailo 0000:01:00.0: Probing: Device enabled
[    6.203884] hailo 0000:01:00.0: Probing: mapped bar 0 - 00000000f4d4cc4f 16384
[    6.203890] hailo 0000:01:00.0: Probing: mapped bar 2 - 00000000d15eb731 4096
[    6.203894] hailo 0000:01:00.0: Probing: mapped bar 4 - 000000003996c7e5 16384
[    6.203898] hailo 0000:01:00.0: Probing: Setting max_desc_page_size to 4096, (page_size=4096)
[    6.203953] hailo 0000:01:00.0: Probing: Enabled 64 bit dma
[    6.203954] hailo 0000:01:00.0: Probing: Using specialized dma_ops=iommu_dma_ops
[    6.203960] hailo 0000:01:00.0: Probing: Using userspace allocated vdma buffers
[    6.203962] hailo 0000:01:00.0: Disabling ASPM L0s 
[    6.203964] hailo 0000:01:00.0: Successfully disabled ASPM L0s 
[    6.337451] hailo 0000:01:00.0: Firmware was loaded successfully
[    6.350893] hailo 0000:01:00.0: Probing: Added board 1e60-2864, /dev/hailo0

