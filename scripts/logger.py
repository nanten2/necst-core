#!/usr/bin/env python3

name = 'logger'

import sys
import time
import datetime
import threading
sys.path.append("/home/exito/python/oplite")
from oplite import Oplite

import rospy
import std_msgs.msg

class logger(object):

    def __init__(self):
        self.count = 0
        self.flag = ""
        self.log_flag = False
        self.msgtype_dict = {'std_msgs/Int32': std_msgs.msg.Int32,
                             'std_msgs/Float32': std_msgs.msg.Float32}
        _topic_li = rospy.get_published_topics()
        self.topic_li = []
        for i in range(len(_topic_li)):
            if _topic_li[i][0] == '/rosout': pass
            elif _topic_li[i][0] == '/rosout_agg': pass
            elif _topic_li[i][0] == '/test/revolution': pass
            else: self.topic_li.append(_topic_li[i])

    def make_table(self):
        [self.op.make_table('"'+self.topic_li[i][0]+'"', "(data, time float)") 
                for i in range(len(self.topic_li))]
        return

    def callback_data(self, req, args):
        if self.log_flag:
            self.op.write('"'+self.topic_li[args["index"]][0]+'"', "",(req.data,time.time()), cur_num=args["index"], auto_commit=False)
        else: pass
        return

    def callback_flag(self, req):
        self.flag = req.data.upper()
        return

    def log(self):
        while not rospy.is_shutdown():
            while self.flag == "":
                time.sleep(0.001)
                continue

            if self.flag == "READY":
                t = datetime.datetime.fromtimestamp(time.time())
                dbpath = '/home/exito/data/logger/{}.db'.format(t.strftime('%Y%m%d_%H%M%S'))
                self.op = Oplite(dbpath, len(self.topic_li))
                self.make_table()
                print("DATABASE OPEN")
                self.log_flag = False
            else: pass
            
            if self.flag == "START":
                self.log_flag = True
            elif self.flag == "END":
                self.log_flag = False
                self.op.commit_data()
                self.op.close()
                print("DATABASE CLOSE")
            else: pass

            self.flag = ""
        return

    def start_thread(self):
        th = threading.Thread(target=self.log)
        th.setDaemon(True)
        th.start()


if __name__ == '__main__':
    rospy.init_node(name)
    
    logg = logger()
    logg.start_thread()

    
    flag = rospy.Subscriber(
        name = '/logger_flag',
        data_class = std_msgs.msg.String,
        callback = logg.callback_flag,
        queue_size = 1,
    )

    topic_from = [rospy.Subscriber(
                name = logg.topic_li[i][0],
                data_class = logg.msgtype_dict[logg.topic_li[i][1]],
                callback = logg.callback_data,
                callback_args = {'index': i },
                queue_size = 1,
            ) for i in range(len(logg.topic_li))]

    rospy.spin()
