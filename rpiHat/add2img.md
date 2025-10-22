# chroot into a Raspberry Pi image

* to add packages to a Raspberry Pi image, chroot into the image and install the packages

```

sudo apt install qemu qemu-user-static binfmt-support

xz -d  2024-10-22-raspios-bookworm-arm64-full.img.xz

truncate -s +5G 2024-10-22-raspios-bookworm-arm64-full.img
sudo losetup -P /dev/loop20 2024-10-22-raspios-bookworm-arm64-full.img
sudo gparted /dev/loop20
sudo losetup -d /dev/loop20

sudo mount -o loop,offset=$((512 * 1056768)) 2024-10-22-raspios-bookworm-arm64-full.img /mnt2/


sudo cp /usr/bin/qemu-aarch64-static  /mnt2/usr/bin/
sudo cp /etc/resolv.conf /mnt2/etc/

sudo mount -o bind /dev /mnt2/dev
sudo mount -o bind /sys /mnt2/sys
sudo mount -o bind /proc /mnt2/proc
sudo mount -o bind /dev/pts /mnt2/dev/pts

sudo chroot /mnt2 /bin/bash


sudo umount /mnt2/dev /mnt2/sys /mnt2/proc /mnt2/dev/pts /mnt2 

````