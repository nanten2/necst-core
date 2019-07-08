#!usr/bin/env python3

name  = 'db_logger_always'

import time
import threading
import necstdb

import rospy
import std_msgs.msg

class db_logger_always(object):

    def __init__(self):
        self.db_path = '/home/exito/data/logger/test/20190708/1500-always.db'
        self.last_append_time = 0

        self.th = threading.Thread(target= self.loop)
        self.th.start()
        pass

    def regist(self, data):
        if time.time() -  self.last_append_time >= 10:
            self.data_list.append({'path': self.db_path, 'data': data})
            self.last_append_time = time.time()
            pass
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
            # if os.path.exits(self.dbpath[:self.dbpath.rfind('/')]):pass
            # else: os.makedirs(self.dbpath[:self.dbpath.rfind('/')]) 
            # self.db =necstdb.necstdb(self.dbpath,len(data))
            self.db.insert(d)
            continue 
        return   
