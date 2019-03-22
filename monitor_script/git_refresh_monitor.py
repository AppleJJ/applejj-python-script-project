_author__ = 'applejj'
#!/usr/bin/env python
#coding:utf-8

import sys
import os
import re
import traceback
import subprocess
from shutil import *
import urllib2
import tarfile

defaultencoding = 'utf-8'

def run_cmd(cmd):
    try:
        return_code = 0;
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return_code = e.returncode
        output = e.output
    return (cmd, return_code, output)

if __name__ == '__main__':

    if sys.getdefaultencoding() != defaultencoding:
        reload(sys)
        sys.setdefaultencoding(defaultencoding)

    if len(sys.argv) != 2:
        print" usage: python get_tar_file_untar.py automation"

    project_name = sys.argv[1]
    if project_name == '*-automation':
        git_url = 'ssh://git@*-automation.git'
    elif project_name == 'mobileautomation':
        git_url = 'ssh://*/mobi-automation.git'

    command = '''cd /tmp; git clone %s'''% (git_url)
    print command
    (command, return_code, output) = run_cmd(command)

    command = '''cd /tmp; mv %s /usr/ipts/''' % (project_name)
    (command, return_code, output) = run_cmd(command)

    command = '''cd /*/; chmod -R 777 %s; chown -R *:nagios %s''' % (project_name,project_name)
    (command, return_code, output) = run_cmd(command)






