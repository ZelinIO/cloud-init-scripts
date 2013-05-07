#!/bin/sh
parms="/etc/cloud/local/parms"
start=$(fdisk -l /dev/vda | grep vda2 | awk '{print $3}')
echo $start
#echo -e "d" > $parms
#echo -e "3" >> $parms
echo -e "n" >> $parms
echo -e "p" >> $parms
echo -e "3" >> $parms
echo -e $start >> $parms
echo -e "" >> $parms
echo -e "w" >> $parms
  
fdisk /dev/vda < $parms
touch /etc/cloud/local/has_partitioned
echo -e "re_partion" >> /etc/cloud/order.log
#reboot
#sleep 10s

