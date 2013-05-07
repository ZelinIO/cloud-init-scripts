# Copyright (c) 2013, Zelin.io
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

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
reboot
#sleep 10s

