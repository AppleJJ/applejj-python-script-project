#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import os
import urllib2
import sys, urllib, os, shutil, re
import csv
from math import sqrt, pi, asin, sin, cos, atan2
from datetime import *
import types
import socket
import fcntl
import struct
import json
import commands
import hmac
from hashlib import sha1
import base64
import time
import requests


def getAuthorization(uri, method, data, clientid, secret):
    try:
        stringToSign = method + " " + uri + '\n' + data
        signatur = getSignature(bytearray(stringToSign,'utf8'), bytearray(secret,'utf8'))
        return "MWS" + " " + clientid + ":" + signatur
    except Exception, e:
        print ('Exception is: %s') % (repr(e))

def getSignature(data, key):
    rawHmac = hmac.new(key, data, sha1).digest()
    rawHmac = base64.b32encode(rawHmac)
    return rawHmac

def getAuthDate():
    DATE = commands.getoutput('/usr/bin/env TZ=\'GMT\' LANG=en_US date "+%a, %d %b %Y %H:%M:%S %Z"')
    dftime = DATE
    return dftime

def getSignature(data, key):
    rawHmac = hmac.new(key, data, sha1).digest()
    rawHmac = base64.b32encode(rawHmac)
    return rawHmac


def get_config(owner, owner_key, key_name):
    dftime = getAuthDate()
    auth = getAuthorization('/config2/get', 'GET', dftime, owner, owner_key)
    url = 'http://sf/get?env=test&key=%s' % (key_name)
    header_get = {"Date": dftime, "Authorization": auth}
    req = urllib2.Request(url, headers=header_get)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return  the_page

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Useage: python get_schema.py ) path"
        print "path is the folder you want to put the schema"
        sys.exit(1)
    biz= sys.argv[1]
    path= sys.argv[2]

    res = get_lion_config("***","***","***")
    #匹配到ip
    strPattern = re.compile("\d+\.\d+\.\d+\.\d+")
    strMatch = strPattern.search(res)
    ip= strMatch.group()
    #匹配到数据库
    strPattern = re.compile("/[A-Za-z]+")
    strMatch = strPattern.search(res)
    db= strMatch.group().strip("/")
    #获取用户名
    res = get_lion_config("***","***","LionDataSource.***")
    user= res.split('"result":')[1].strip("}").strip('"')
    #获取密码
    res = get_lion_config("***","***","***")
    password= res.split('"result":')[1].strip("}").strip('"')

    #导出scheme文件
    sql1= "mysql -h " + ip + " -u " + user + " -p'" + password + "' -D " + db + " --default-character-set=utf8 -e 'SELECT IndexSchema FROM $ where AppName = \"" + biz + "\" order by UpdateTime desc limit 1;' > " + path + "schema.xml"
    os.system(sql1)
    sql2= "mysql -h " + ip + " -u " + user + " -p'" + password + "' -D " + db + " --default-character-set=utf8 -e 'SELECT JoinSource FROM $.$ where AppName = \"" + biz + "\" order by UpdateTime desc limit 1;' > " + path + "joinsource.xml"
    os.system(sql2)
    sql3= "mysql -h " + ip + " -u " + user + " -p'" + password + "' -D " + db + " --default-character-set=utf8 -e 'SELECT IncSource FROM $.$ where AppName = \"" + biz + "\" order by UpdateTime desc limit 1;' > " + path + "incsource.xml"
    os.system(sql3)
    command1 = "sed -i.bak '1d;s/\\\\n//g' " + path + "schema.xml"
    os.system(command1)
    command2 = "sed -i.bak '1d;s/\\\\n//g' " + path + "joinsource.xml"
    os.system(command2)
    command3 = "sed -i.bak '1d;s/\\\\n//g' " + path + "incsource.xml"
    os.system(command3)


