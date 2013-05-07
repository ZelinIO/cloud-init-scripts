#!/bin/sh

if [[ $# -ne 1 ]]
then
  echo "Usage: chpw.sh password"
  exit 1
fi
passwd=$1
echo "${passwd}" | passwd --stdin root
#echo "${passwd}"

