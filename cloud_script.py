#!/usr/bin/python

from subprocess import call
import json
import urllib2
import platform
import re
import logging
import datetime
import sys
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("/etc/cloud/cloud_init_script.log"))

LOCAL_DATA_PATH = "/etc/cloud/local/data"
META_URL = "http://169.254.169.254/openstack/2013-04-04/meta_data.json"
SCRIPTS_DIR = "/etc/cloud/scripts/"

def _change_password(passwd):
    exe_script = '%schpw.sh "%s"' % (SCRIPTS_DIR, passwd)
    call(exe_script.encode('unicode-escape'), shell=True) 

def change_password(passwd, p_server_date):
    try:
        f = open(LOCAL_DATA_PATH, "r")
        p_local_date = json.load(f)['password_date']
        if p_local_date != p_server_date:
            f.close()
            with open(LOCAL_DATA_PATH, "w") as nf:
                _change_password(passwd)
                json.dump({"password_date" : p_server_date}, nf)
    except (IOError, ValueError) as e:
        with open(LOCAL_DATA_PATH, "w") as f:
            _change_password(passwd)
            json.dump({"password_date" : p_server_date}, f)
    except Exception as e:
        logger.error("Error during updating password! %s" % str(e))
        sys.exit("Script exit unexpectedly!")


def resizefs():
    try:
        exe_script = SCRIPTS_DIR + "resizefs.sh"
        if os.path.exists(exe_script):
    	    call("/etc/cloud/scripts/resizefs.sh", shell=True)
    except Exception as e:
        logger.error("Error during resize fs! %s" % str(e))
        sys.exit("Script exit unexpectedly!!")


try:
    respose = urllib2.urlopen(META_URL)
    data = respose.read()
    data_dict = json.loads(data)
    passwd = data_dict['meta']['password']
    p_server_date = data_dict['meta']['password_date']
    change_password(passwd, p_server_date)
#    resizefs()

except Exception as e:
    logger.info("%s\n" % str(e))
    sys.exit("Script exit unexpectedly!")



