#!usr/bin/env python3

name  = 'db_app'

import os
import time
import datetime
import threading
import necstdb

import rospy
import std_msgs.msg

class db_logger_operation(object):

    def __init__(self):
        self.data_list = []
        self.db_path = ''
        self.db = necstdb.necstdb()
        self.sub_path = rospy.Subsciber(
            name = '/logger_path',
            data_class = std_msgs.msg.String,
            callback = self.callback_path,
            queue_size = 1,
        )
        self.th = threading.Thread(target=self.loop)
        self.th.start()
        pass


    def callback_path(self, req):
        if req.data =='':
            self.action_flag = False
   
        else:
            if self.dp_path == '':
                self.action_flag = True
                self.db_path = req.data
            else:
                # angry code    
                pass
                   
            pass 
        return

    def regist(self, data):
        if self.action_flag:
            self.data_list.append(data)
            pass
      
        return

    def loop(self):
        while True:    
            if len(self.data_list) == 0:
                if self.action_flag == False:
                    self.db.finalize()
                    self.db_path = ''
                    pass
                    
                if rospy.is_shutdown():
                    break
                time.sleep(0.01)
                continue

            d = self.data_list.pop(0)
            # if os.path.exits(self.dbpath[:self.dbpath.rfind('/')]):pass
            # else: os.makedirs(self.dbpath[:self.dbpath.rfind('/')]) 
            # self.db =necstdb.necstdb(self.dbpath,len(data))
            self.db.insert(self.db_path, d['topic_name'], d['msg'])
            continue 

        self.db.finalize()
        return            

            
