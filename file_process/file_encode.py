#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib

data=open('/Users/applejj/Desktop/mtTest.csv','r')
out=open('/Users/applejj/Desktop/mtTest.csv.encode','w')

for line in data:
    string1=urllib.quote(line)
    string1.replace("%0A","\n")
    out.write(string1)
    out.write('\n')


data.close()
out.close()