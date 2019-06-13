#!/usr/bin/env python3

name = 'db_logger'

import sys, os
import time
import datetime
import threading
import necstdb

import rospy
import std_msgs.msg

class db_logger(object):

    def __init__(self):
        self.db_path = ''
        self.log_flag = False
        self.topic_li = self.make_topic_li()
        self.msgtype_dict = {
            'std_msgs/Int32': std_msgs.msg.Int32,
            'std_msgs/Float64': std_msgs.msg.Float64,
        }

    def make_topic_li(self):
        topic_li = []
        _topic_li = rospy.get_published_topics()
        for i in range(len(_topic_li)):
            if _topic_li[i][0] == '/rosout': pass
            elif _topic_li[i][0] == '/rosout_agg': pass
            else: topic_li.append(_topic_li[i])
        return topic_li

    def make_table(self):
        [self.db.make_table('"'+self.topic_li[i][0]+'"', "(data, time float)") 
            for i in range(len(self.topic_li))]
        return

    def callback_data(self, req, args):
        if self.log_flag:
            self.db.write('"'+self.topic_li[args["index"]][0]+'"', "",
                (req.data,time.time()), cur_num=args["index"], auto_commit=False)
        else: pass
        return

    def callback_flag(self, req):
        self.db_path = req.data
        return

    def log(self):
        while not rospy.is_shutdown():
            while self.db_path == '':
                time.sleep(0.001)
                continue

            if os.path.exists(db_path[:path.rfind('/')]): pass
            else: os.makedirs(db_path[:path.rfind('/')])
            self.db = necstdb.necstdb(self.db_path, len(self.topic_li))
            self.make_table()
            print("DATABASE OPEN")
            self.log_flag = True

            while self.db_path != '':
                time.sleep(0.001)
                continue

            self.db.commit_data()
            self.db.close()
            print("DATABASE CLOSE")
            self.log_flag = False
        return

    def start_thread(self):
        th = threading.Thread(target=self.log)
        th.setDaemon(True)
        th.start()


if __name__ == '__main__':
    rospy.init_node(name)
    
    logg = db_logger()
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
