#!usr/bin/env python3

name  = 'db_logger_operation'

import time
import threading
import necstdb

import rospy
import std_msgs.msg

class db_logger_always_vol2(object):

    def __init__(self):
        self.data_list = []
        self.db_path = '/home/exito/data/logger/test/20190708/kondo-always.db'
        self.db = necstdb.necstdb()
        self.th = threading.Thread(target= self.loop)
        self.th1 = threading.Thread(target= self.make_temp_data)

        self.th.start()
        self.th1.start()
        pass


    def callback_path(self, req):
        self.db_path = req.data
        return

    def regist(self, data):
        if self.db_path != '':
            self.data_list.append({'path': self.db_path, 'data': data})
        else: pass

        return

    def make_temp_data(self,t=10):
        while True:
            self.temp_data_list = []
            st = time.time()
            while time.time()-st < t:
                d = self.data_list.pop(0)
                topic = list(d["data"].keys())
                data = d["data"][str(topic)]

                list_num = len(temp_data_list)
                list_topic = []
                for i in range(list_num):
                    s = list(temp_data_list[i].keys())
                    list_topic.append(s[0])

                for i in range(len(list_topic)):
                    if topic not in list_topic:
                        self.temp_data_list.append(d)
                    else:
                        index = list_topic.index(topic)
                        self.temp_data_list[index]["data"][topic] = d[topic]

    def loop(self):

        while True:
            if len(self.temp_data_list) == 0:
                self.db.finalize()
                pass

                if rospy.is_shutdown():
                    break
                time.sleep(0.01)
                continue

            d = self.temp_data_list.pop(0)
            # if os.path.exits(self.dbpath[:self.dbpath.rfind('/')]):pass
            # else: os.makedirs(self.dbpath[:self.dbpath.rfind('/')])
            # self.db =necstdb.necstdb(self.dbpath,len(data))
            d_list = []

            self.db.insert(d)
            continue
        return
