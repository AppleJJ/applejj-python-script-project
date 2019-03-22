__author__ = 'applejj'
#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import commands
import re
import os
import urllib
import smtplib
import string
import urllib2
import json
from ftplib import FTP
import difflib
import argparse

reload(sys)
sys.setdefaultencoding('utf8')


def run_cmd(cmd):
    try:
        return_code = 0;
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return_code = e.returncode
        output = e.output
    return (cmd, return_code, output)


def ftpconnect(host, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp

def downloadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)
    fp.close()

def uploadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()

def readfile(filename):
    try:
        with open(filename, 'r') as fileHandle:
            text = fileHandle.read().splitlines()
        return text
    except IOError as e:
        print("Read file Error:", e)
        sys.exit()

def diff_file(filename1, filename2):
    text1_lines = readfile(filename1)
    text2_lines = readfile(filename2)
    d = difflib.HtmlDiff()
    result = d.make_file(text1_lines, text2_lines, filename1, filename2, context=False)
    with open('result.html', 'w') as resultfile:
        resultfile.write(result)
        # print(result)



def getdiffcodefile(project_name):
    command = '''cd /data/home/jenkins/%s; git whatchanges --since "1 weeks agp" >/tmp/codediff.log ''' % (project_name)
    print command
    (command, return_code, output) = run_cmd(command)
    command = '''grep ".java" /tmp/codediff.log | awk "{print $6}" '''


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print "usage: xxx.py project_name"
        sys.exit(1)

    file_orginal =sys.argv[1]
    file_now= sys.argv[2]

    diff_file(file_orginal,file_now)
