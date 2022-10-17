#!/user/bin/python
# -*- coding:utf-8 -*-

import requests
import xlsxwriter

report_file = xlsxwriter.Workbook("data.xlsx")
worksheet = report_file.add_worksheet()
worksheet.wirte("A1","app_name")
worksheet.write("B1","service")
worksheet.write("C1","method")

service_name = 'abc'
row_index= 2

request_app_name = 'http://%sXXX' %(service_name)

headers = {'Content-Type':'application/json'}

response = requests.get(url= request_app_name, params= headers)
response_json = response.json()
services = response_json["services"]

for service in services:
	index1="B%s" % row_idnex
	worksheet.write(index1, service)

	request_data = "http://XXX%s" % service
	response_service = requests.get(url = request_data, params = headers)
	request_data_json = response_service.json()
	methods = request_data_json["XXX"]
	length = len(methods)
	for index in range(length):
		index2 = "C%s" %row_index
		worksheet.write(index2,methods[index]["XXX"])
		row_index += 1

report_file.close()