Cloud-init-scripts
===============
These scripts are based on cloud-init to setup the initial root password and re-configurate disk partitions automatically. (For Zelin Openstack)

This document details how to make Linux image with our cloud-init-scripts in Zelin. CentOS-6.4 is used as an example here, but it should not be limited to any specific Linux distribution.

# Install OS in VM #
* create VM image by `qemu-img create -f raw <image-name> <size>`  
* install CentOS from ISO. (Note: Do not enable virtio during the whole installation; make sure to allocate 1G mem at least for the VM)
* In the hard disk partition step of installation, make sure to create two primary partitions: one (1~2GB) for swap and the other for the "/". 
* After complete installation, enable virtio to reboot VM.

# Install Software packages #
In case the VM eth[x] is not enabled, try to configure `/etc/sysconfig/network-scripts/ifcfg-eth[x]` to `OnBoot=yes` and reboot VM. Make sure eth[x] get an ip and is able to access public resource. 
* `yum install cloud-init python-pip`
Note: If no cloud-init is found, try a different yum repo or download cloud-init from official site.

# Configuration #
* Download a copy of [cloud-init-scripts](https://github.com/ZelinIO/cloud-init-scripts/archive/master.zip)
Unzip the zip-ball
```
chmod +x *.py
chmod +x *.sh
./install.py (if any error occurs, retry it after ./uninstall.sh)
```

* reboot VM. This step cloud-init will be initialized. (Probably, during VM startups it will throw server (169.254.169.254) connection errors and take a couple of minutes polling. Be patient and take it easy to wait for it timeout.:)  

* edit `/etc/udev/rules.d/70-persistent-net.rules` and remove all the eth[x] entries. (This is especially for CentOS)    

ps:   
1. In CentOs, if you don't remove eth[x] entry in this file, when the image is launched by openstack, the NIC created by openstack will not be eth0, which makes cloud-init not working correctly.   
2. For other Linux distributions, please check if you need do this step.

* edit `/etc/sysconfig/network-scripts/ifcfg-eth[x]`
```
OnBoot=yes
NM_Controller=no
remove HWADDR, UUID
```
* `history -c` to clear all the history commands.

# Shutdown VM #
Shutdown VM, Not reboot vm!
The image is ready for glance and cinder. 