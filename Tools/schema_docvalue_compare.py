#!/usr/bin/python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import re
import string
import sys



tree =ET.ElementTree(file='/*/schema.xml')
root=tree.getroot()
dict_schema = {}
dict_java = {}
dict_constant={}

date_java=open('/*/main/java/com/dp/arts/s*lues.java','r')
data_constant=open('/*scorer/src/main/java/c*/FieldName.java','r')

for child_of_root in root:
    name = child_of_root.get('name')
    type = child_of_root.get('type')
    docvalues = child_of_root.get('docvalues')
    dict_schema[name] = type

for line in date_java:
    if not line.find('docValues = (DpDocValues) reader.docValues(FieldName.') == -1:
        name = re.sub('docValues = \(DpDocValues\) reader.docValues\(FieldName.',"",line)
        name = re.sub('\);','',name)
        #name = string.lower(name)
        name = name.strip()
    if not line.find('docValues.setDpType(DpType.') == -1:
        type = re.sub('docValues.setDpType\(DpType.', "", line)
        type = re.sub('\);',"",type)
        type = string.lower(type)
        type = type.strip()
        #print type
        #print name
        dict_java[name] = type

for line in data_constant:
    if not line.find('public static final String') == -1:
        key_value = re.sub('public static final String',"",line)
        key_value = key_value.strip()
        key = key_value.split('=')[0].strip()
        value = re.sub('"','',key_value.split('=')[1])
        value = re.sub(';','',value)
        value = value.strip()
        dict_constant[key] = value

print dict_constant
print dict_java
print dict_schema
print '___________________________'

for key in dict_java:
    type_java = dict_java[key]
    key_schema = dict_constant[key]
    type_schema = dict_schema[key_schema]
    if type_java == type_schema:
        flag = 'ture'
        #print flag
    else:
        flag = 'false'
        print ('%s字段的类型不一致,分别为java:%s,schema:%s' % (key_schema,type_java,type_schema))
        #sys.exit(0)
    #print flag


