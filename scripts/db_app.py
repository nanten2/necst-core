#!usr/bin/env python3

name  = 'db_app'

import os
import time
import datetime
import threading
import necstdb

import rospy
import std_msgs.msg

class db_app(object):

    def __init__(self):
        self.db_path = ''
        self.path = rospy.Subsciber(
                name = '/logger_path',
                data_class = std_msgs.msg.String,
                callback = self.callback_path,
                queue_size = 1,
                )
        self.th = threading.Thread(target=self.loop)
        self.th.start()
    


    def callback_path(self,req):
        if req.data =='':
            self.flag = False
        else:
            self.flag = True
            self.dbpath = req.data

    def func1(self,arg):
        if self.flag:
            arglist = arglist.append(arg)

        else:pass
        return

    def loop(self):
        while len(arglist) !=0:
            if os.path.exits(self.dbpath[:self.dbpath.rfind('/')]):pass
            else: os.makedirs(self.dbpath[:self.dbpath.rfind('/')])
          
            a = arglist.pop[0]
            self.db =necstdb.necstdb(self.dbpath,len(a))
            self.db.write(topic_name,data,self.dppath)

          continue

         self.path =''

         if rospy.is_shutdown():
             pass
         else:
             time.sleep(0.01)
         return

            
