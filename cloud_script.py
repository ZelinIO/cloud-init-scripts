#!/usr/bin/python

from subprocess import call
import json
import urllib2
import platform
import re
import logging
import datetime
import iso8601
import sys
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("/etc/cloud/cloud_init_script.log"))

LOCAL_DATA_PATH = "/etc/cloud/local/data"
META_URL = "http://169.254.169.254/openstack/2013-04-04/meta_data.json"
SCRIPTS_DIR = "/etc/cloud/scripts/"

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
PERFECT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def parse_isotime(timestr):
    """Parse time from ISO 8601 format"""
    try:
        return iso8601.parse_date(timestr)
    except iso8601.ParseError as e:
        raise ValueError(e.message)
    except TypeError as e:
        raise ValueError(e.message)


def normalize_time(timestamp):
    """Normalize time (datetype) in arbitrary timezone to UTC naive object"""
    offset = timestamp.utcoffset()
    if offset is None:
        return timestamp
    return timestamp.replace(tzinfo=None) - offset

def timestampfromutc(utc):
    delta = normalize_time(utc) - datetime.datetime.utcfromtimestamp(0)
    return ((delta.days * 24 * 3600) + delta.seconds + float(delta.microseconds) / (10 ** 6))

def _change_password(passwd):
    exe_script = '%schpw.sh "%s"' % (SCRIPTS_DIR, passwd)
    call(exe_script.encode('unicode-escape'), shell=True) 

def change_password(passwd):
    try:
        f = open(LOCAL_DATA_PATH, "r")
        p_local_stamp = json.load(f)['password_date']
        if p_local_stamp < p_server_stamp:
            f.close()
            with open(LOCAL_DATA_PATH, "w") as nf:
                _change_password(passwd)
                json.dump({"password_date" : p_server_stamp}, nf)
    except (IOError, ValueError) as e:
        with open(LOCAL_DATA_PATH, "w") as f:
            _change_password(passwd)
            json.dump({"password_date" : p_server_stamp}, f)
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
    p_server_stamp = timestampfromutc(parse_isotime(p_server_date))
    change_password(passwd)
#    resizefs()

except Exception as e:
    logger.info("%s\n" % str(e))
    sys.exit("Script exit unexpectedly!")



