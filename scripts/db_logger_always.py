#!usr/bin/env python3

name  = 'db_logger_always'

import time
import datetime
import threading
import necstdb

import rospy
import std_msgs.msg

class db_logger_always(object):

    def __init__(self):
        self.db_path = '/home/exito/data/logger/always/'
        self.last_append_time = 0
        self.current_topic_list = []
        self.data_list = []
        self.receive_time_dic ={}

        self.db = necstdb.necstdb()
        self.th = threading.Thread(target= self.loop)
        self.th.start()
        pass

    def regist(self, data):
        self.data_list.append({'path': "", 'data': data})
        return

    def loop(self):
        while True:    
            if len(self.data_list) == 0:
                self.db.finalize()
                pass
                    
                if rospy.is_shutdown():
                    break
                time.sleep(0.01)
                continue
            
            d = self.data_list.pop(0)
            d['path'] = self.db_path + "{0:%Y%m%d}.db".format(datetime.datetime.now())
            
            if d['data']['topic'] not in self.receive_time_dic:
                self.receive_time_dic[d['data']['topic']] = d['data']['time']
                self.db.insert(d)
                pass
            
            if self.receive_time_dic[d['data']['topic']] - d['data']['time'] >= 10:
                self.db.insert(d)
                self.receive_time_dic[d['data']['topic']] = d['data']['time']
            continue 
        return   
