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
        call("rm -rf retfile", shell = True)
    else:
        call("rm -rf retfile", shell = True)
        print "Virtio is not installed!\n"
        sys.exit("Terminated unexpectedly!\n")
    
except Exception as e:
    print str(e)
    sys.exit("Terminated unexpectedly!\n")

print "\nBingo! Cloud-init configuration is deployed successfully!\n"
