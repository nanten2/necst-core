#!/usr/bin/env python3

name = 'db_full'

import os
import time
import datetime
import threading
import necstdb

import rospy
import std_msgs.msg

class db_full(object):

    def __init__(self):
        self.db_path = ''
        self.log_flag = False
        self.path = rospy.Subscriber(
                name = '/logger_path',
                data_class = std_msgs.msg.String,
                callback = self.callback_path
                queue_size = 1,
                )
      
    def func1(self,arg):
        argslist = argslist.append(arg)
        return

    def callback_path(self,req):
        self.db_path = req.data
        return
return
    def loop(self):
        while not rospy.is_shutdown():
            while self.db_path == '':
                 while not rospy.is_shutdown():
                    a = arglist.pop[0]
                    time.sleep(0.001)
                    break
                 continue

            if os.path.exits(self.db_path[:self.db_path.rfind('/')]):pass
            else: os.makedirs(self.db_path[:self.db_path.rfind('/')])
            self.db =necstdb.necstdb(self.db_path,len(a[0]))
        
            while self.db_path != '':
                while not rospy.is_shutdown():
                    time.sleep(0.001)
                    break
                continue
            
           self.db.close()
        return


            


