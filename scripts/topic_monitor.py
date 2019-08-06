#! /usr/bin/env python3

name = 'topic_monitor'

# ----
import threading

import rospy
import time
import std_msgs.msg

class topic_monitor(object):

    def __init__(self):
        self.topic_dic = {} #{'topic1':data1,'topic2':data2, ...}
        self.th = threading.Thread(target= self.loop)
        self.th.start()
        print("tmmonitor")
        pass


    def regist(self, data):
        #data = {'topic': arg,'received_time': time.time(), 'slots': [{'key': key,'type', type,'values': req.data}]}
        if len(data[slots]) == 1:
            self.topic_dic[data["topic"]] = data["slots"]["values"]
            pass
        return

    def loop(self):
        while not rospy.is_shutdown():
            print("------------------")

            for topic, data in sorted(self.topic_dic.items()):
                print(topic+" : %s"%(data]))
                time.sleep(0.1)

            continue
        return


    def thread(self):
        th = threading.Thread(target=self.loop)
        th.setDaemon(True)
        th.start()


if __name__=='__main__':
    rospy.init_node(name)
    tm = topic_monitor()
    tm.thread()
    rospy.spin()
