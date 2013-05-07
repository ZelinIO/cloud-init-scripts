#!/bin/sh

if [[ $# -ne 1 ]]
then
  echo "Usage: cloud_linux.sh password"
  exit 1
fi
passwd=$1
echo "${passwd}" | passwd --stdin root
echo "${passwd}"

#echo -e "start to run resizefs" >> /etc/cloud/order.log
#/etc/cloud/scripts/resizefs.sh
#echo -e "end to resizefs" >> /etc/cloud/order.log

