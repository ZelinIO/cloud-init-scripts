#!/usr/bin/python

import os
from subprocess import call
import sys


def _deply_cfg():
    ret = 0
    ret += call("mkdir /etc/cloud/local 1>testcfg", shell = True)
    ret += call("mkdir /etc/cloud/scripts 1>>testcfg", shell = True)
    ret += call("mkdir -p /var/lib/cloud/scripts/per-boot 1>>testcfg", shell = True)
    ret += call("mkdir -p /var/lib/cloud/scripts/per-once 1>>testcfg", shell = True)
    ret += call("cp cloud.cfg /etc/cloud/", shell = True) 
    ret += call("cp chpw.sh /etc/cloud/scripts", shell = True) 
    ret += call("cp cloud_script.py /var/lib/cloud/scripts/per-boot/", shell = True) 
    ret += call("cp repartition.sh /var/lib/cloud/scripts/per-once/", shell = True) 
    if ret != 0:
        print "Error occur when copying files!\n"
        sys.exit("Terminated unexpectedly!\n")


if not os.path.exists("/etc/cloud"):
    print "Cloud-init is installed incorrectly!\n"
    sys.exit("Terminated unexpectedly!\n")

ret = call("lsmod | grep virtio 1>retfile", shell = True)
try:
    if ret == 0 and os.stat("retfile").st_size >= 0:
        _deply_cfg()
    else:
        print "Virtio is not installed!\n"
        sys.exit("Terminated unexpectedly!\n")
except Exception as e:
    print str(e)
    sys.exit("Terminated unexpectedly!\n")

print "\nBingo! Cloud-init configuration is deployed successfully!\n"
