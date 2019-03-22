#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import json
import sys
import random
import linecache
import os
reload(sys)
sys.setdefaultencoding('utf-8')

data = open("/Users/applejj/Desktop/rec-shopid.csv","r")
out = open("multi_shopids.txt","w")

for i in range(0,3606560):
    #生成一个随即数，为shopid的数量
    shop_list = []
    shopid_num = random.randint(10,50)
    for j in range(0,shopid_num):
        shopid_position = random.randint(0,3606560)
        shopid = linecache.getline("/Users/applejj/Desktop/rec-shopid.csv",shopid_position)
        shopid = shopid.replace('\n','')
        shop_list.append(shopid)

    out.write(str(shop_list))
    out.write("\n")


data.close()
out.close()






