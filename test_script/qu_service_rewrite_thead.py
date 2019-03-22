#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from urllib import urlopen
import json
from urllib import quote
from multiprocessing import Pool
reload(sys)
sys.setdefaultencoding('utf-8')

_curpath = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


full_url = 'http://10.66.39.41:4081/*iteService&method=queryRewrite&parameterTypes=java.lang.String&parameters=%s&parameterTypes=java.lang.String&parameters=%s'


def parse_result(line):
    values = line.split('\t')
    cityid = values[0]
    keyword = values[1]
    real_keyword = values[2]
    try:
        url = full_url % (cityid, keyword)
        page = urlopen(url)
        response = page.read().decode()
        rewrite_length = len(json.loads(response)["qrwRes"])
        if (rewrite_length == 1):
            rewritekeyword = json.loads(response)["qrwRes"][0]["rewriteEntities"][0]["rewriteWord"].encode()
            rewrite_module = json.loads(response)["qrwRes"][0]["rewriteModule"].encode()
            if rewritekeyword == real_keyword and rewrite_module == 'ACCURATE_REWRITE':
                return ("right", "")
            elif rewritekeyword != real_keyword and rewrite_module == 'ACCURATE_REWRITE':
                content = ("%s\t%s\tneed:%s\treal:%s\n") % (cityid, keyword, real_keyword, rewritekeyword)
                return ("wrong", content)
            else:
                content = ("%s\t%s only have FUZZY\n") % (cityid, keyword)
                return ("fuzzy", content)
        elif rewrite_length == 2:
            rewrite_module_1 = json.loads(response)["qrwRes"][0]["rewriteModule"].encode()
            rewrite_module_2 = json.loads(response)["qrwRes"][1]["rewriteModule"].encode()
            if (rewrite_module_1 == 'ACCURATE_REWRITE'):
                rewritekeyword = json.loads(response)["qrwRes"][0]["rewriteEntities"][0]["rewriteWord"].encode()
            if (rewrite_module_2 == 'ACCURATE_REWRITE'):
                rewritekeyword = json.loads(response)["qrwRes"][1]["rewriteEntities"][0]["rewriteWord"].encode()
            if rewritekeyword == real_keyword:
                return ("right","")
            else:
                content = ("%s\t%s\tneed:%s\treal:%s\n") % (cityid, keyword, real_keyword, rewritekeyword)
                return ("wrong", content)
        else:
            content = ("%s\t%s\tneed:%s\treal:null\n") % (cityid, keyword, real_keyword)
            return ("null", content)
    except Exception as err:
        content = ("%s\t%s\tneed:%s\treal:error\n") % (cityid, keyword, real_keyword)
        return ("err", content)

def batch_test():
    test_input = open(_curpath + '/data/rewrite_log/conf_high_qc_dic.txt', 'r').readlines()
    out = open(_curpath + '/data/rewrite_log/test_out.txt', 'wb')
    count_right = 0
    count_null = 0
    count_wrong = 0
    count_fuzzy = 0
    count_err = 0
    pool = Pool(24)
    results = pool.map(parse_result, test_input)
    pool.close()
    pool.join()
    cnt = 0
    for res in results:
        if res is not None:
            if res[0] == "right":
                count_right +=1
            elif res[0] == "wrong":
                out.write(res[1] + '\n')
                count_wrong +=1
            elif res[0] == "null":
                out.write(res[1] + '\n')
                count_null +=1
            elif res[0] == "fuzzy":
                count_fuzzy +=1
                out.write(res[1] + '\n')
            elif res[0] == 'err':
                count_err +=1
                out.write(res[1] + '\n')


    print 'test nums: ', len(test_input)
    print 'right:', count_right, '\twrong:', count_wrong, '\tauc:', count_right/(float)(count_right + count_wrong)
    print 'null:', count_null, '\trecall:', (count_null + count_right + count_wrong)/(float)(len(test_input)- count_err)
    print 'search err', count_err


if __name__ == '__main__':
    print 'begin...'
    batch_test()
    print 'finished!'


