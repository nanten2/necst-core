#!usr/bin/env python3

name  = 'db_logger_operation'

import time
import threading
import necstdb

import rospy
import std_msgs.msg

class db_logger_operation(object):

    def __init__(self):
        self.data_list = []
        self.db_path = ''
        self.db = necstdb.necstdb()
        self.sub_path = rospy.Subscriber(
            name = '/logger_path',
            data_class = std_msgs.msg.String,
            callback = self.callback_path,
            queue_size = 1,
        )
        
        self.th = threading.Thread(target= self.loop)

        self.th.start()
        pass


    def callback_path(self, req):
        self.db_path = req.data
        return

    def regist(self, data):
        if self.db_path != '':
            self.data_list.append({'path': self.db_path, 'data': data})
            print(data)
        else: pass
      
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

        
