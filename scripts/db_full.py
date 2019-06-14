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
        self_msgtype_dict = {
                'std_msgs/Int32': std_msgs.msg.Int32,
                'std_msgs/Float64': std_msgs.msg.Float64
                }

        self.topic_li = rospy.Subscriber(
                name = '/logger_path',
                data_class = std_msgs.msg.String,
                callback = db_full.callback_path
                queue_size = 1,
                )

    def func1(self):


    def callback_path(self,req):
        self.db_path = req.data
        return

    def loop(self):
        while not rospy.is_shutdown():
            while self.db_path == '':
                while not rospy.is_shutdown():
                    time.sleep(0.001)
                    continue

            if os.path.exits(self.db_path[:self.db_path.rfind('/')]):pass
            else: os.makedirs(self.db_path[:self.db_path.rfind('/')])
            self.db =necstdb.necstdb(self.db_path,len(self.topic_li))
        
            while self.db_path != '':
                while not rospy.is_shutdown():
                    time.sleep(0.001)
                    continue
            
           self.db.close()
        return


            


