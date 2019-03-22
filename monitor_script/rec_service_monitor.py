#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import string
import json
import codecs
import time
import commands
import base64
import hashlib
import hmac
import requests
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')


def check_service_status(hostname, bizname, port, query, expectTotalhits, appname):
    fi = codecs.open('/data/applogs/rec.log', 'a', encoding='utf-8')
    datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    fi.write('datetime:%s' % datetime)
    url = "http://%s:%s/search/%s?%s" % (hostname, port, bizname, query)
    fi.write('url:%s\n' % url)
    fi.close()
    mark_status_url = "%s:%s/tatus&app=%s" % (hostname, port, bizname)
    check_url_totalhits_time(hostname, url, expectTotalhits, mark_status_url, appname)


def check_url_totalhits_time(hostname, url, expectTotalhits, mark_status_url, appname):
    cmd = 'curl \'%s\'' % (url)
    response_time = 1000
    response = os.popen(cmd).read()
    if ("totalhits" in response):
        json_response = json.loads(response)
        totalhits = json_response.get("totalhits")
        print totalhits
        try:
            response_time = json.loads(response.decode())["otherinfo"]["executiontime"].encode()
            print response_time
            response_time = int(response_time)
        except:
            print 'there is some question'


        if (totalhits >= expectTotalhits):
            print "service is OK"
        else:
            content = 'The Request has Some Problem:%s' % (url)
            # 数据库中记录
            inster_record_to_database(appname, 1, 2)
            send_elephant_notice(content)
            check_service_by_markstatus(hostname, mark_status_url, appname)

        if (response_time < 2000):
            print "service response time is ok"
        else:
            content = 'The Request:%s response time is %s' % (url, response_time)
            inster_record_to_database(appname, 3, 2)
            send_elephant_notice(content)

    else:
        check_service_by_markstatus(hostname, mark_status_url, appname)


def check_service_by_markstatus(hostname, mark_status_url, appname):
    cmd = 'curl \'%s\'' % (mark_status_url)
    print cmd
    markstatus = os.popen(cmd).read()
    if ("up" in markstatus):
        print 'Everything is OK'
    else:
        time.sleep(10)
        markstatus = os.popen(cmd).read()
        if ("up" in markstatus):
            print 'Everything is OK'
        else:
            print "service has some problem"
            # 数据库中记录
            inster_record_to_database(appname, 2, 2)
            content = 'The Service is Down:%s' % (mark_status_url)
            send_elephant_notice(content)


def send_elephant_notice(content):
    timestamp = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())


def gen_headers(client_id, client_secret, url_path, http_method):
    timestamp = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
    string_to_sign = ('%s %s\n%s' % (http_method, url_path, timestamp))
    hmac_bytes = hmac.new(bytes(client_secret.encode('ascii')),
                          bytes(string_to_sign.encode('ascii')),
                          hashlib.sha1).digest()
    auth = base64.b64encode(hmac_bytes).decode("utf-8")
    return {
        'Date': timestamp,
        'Authorization': 'MWS %s:%s' % (client_id, auth),
        'Content-Type': 'application/json;charset=utf-8',
    }


def inster_record_to_database(appname, type, status):
    db = MySQLdb.connect(host="1***", port=3306, user="000", passwd="***",
                         db="***", charset='utf8')
    cursor = db.cursor()
    sql_exect = 'INSERT INTO * (Status, AddTime, UpdateTime) VALUES ("%s",%s,%s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);' % (
        appname, type, status)
    sql = """%s""" % (sql_exect)
    print sql
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()


if __name__ == '__main__':
    feeds_query = '*219.234,LibraABTestInfo:,loccityid:1,adinfe:1'
    check_service_status('10.73.244.125', 'feeds', '*', feeds_query, 100, '*')
    check_service_status('search-aggregator-***.beta', '***', '7771', 'query=all()', 100,
                         'search-aggregator-*')
    # send_elephant_notice('Test is OK')
