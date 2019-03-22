#! /usr/bin/env python
#encoding=utf-8

import threadingtest
import time
from Queue import Queue
import os
import sys

def initQueue(cmd_list):
    global queue
    for line in cmd_list:
        queue.put(line)

class Consumer(threadingtest.Thread):
    def run(self):
        global queue
        while queue.qsize() > 0:
            cmd = queue.get()
            msg = self.name + '执行了 '+ cmd
            os.system(cmd)

queue = Queue()

if __name__ == '__main__':
    cmd_list=[]
    for i in range(2, len(sys.argv)):
        if(sys.argv[1]=="start"):
            if   ("bizer" in sys.argv[i]):
                cmd_list.append("/data/webapps/"+sys.argv[i]+"/bin/biz_server.sh start");
            elif ("searcher" in sys.argv[i]):
                cmd_list.append("/data/webapps/"+sys.argv[i]+"/bin/search_server.sh start");
            elif ("aggregator" in sys.argv[i]):
                cmd_list.append("/data/webapps/"+sys.argv[i]+"/bin/search_server.sh start");
            elif ("supervisor" in sys.argv[i]):
                cmd_list.append("/data/webapps/"+sys.argv[i]+"/bin/supervisor_server.sh start");
            elif ("indexer" in sys.argv[i]):
                cmd_list.append("/data/webapps/"+sys.argv[i]+"/bin/index_server.sh start");
            else:
                print("The paramater of server command is error~~~");
        else:
            if   ("bizer" in sys.argv[i]):
                cmd_list.append("/data/webapps/"+sys.argv[i]+"/bin/biz_server.sh stop");
            elif ("searcher" in sys.argv[i]):
                cmd_list.append("/data/webapps/"+sys.argv[i]+"/bin/search_server.sh stop");
            elif ("aggregator" in sys.argv[i]):
                cmd_list.append("/data/webapps/"+sys.argv[i]+"/bin/search_server.sh stop");
            elif ("supervisor" in sys.argv[i]):
                cmd_list.append("/data/webapps/"+sys.argv[i]+"/bin/supervisor_server.sh stop");
            elif ("indexer" in sys.argv[i]):
                cmd_list.append("/data/webapps/"+sys.argv[i]+"/bin/index_server.sh stop");
            else:
                print("The paramater of server command is error~~~");

    initQueue(cmd_list)
    size = queue.qsize()
    for i in range(size):
        c = Consumer()
        c.start()

