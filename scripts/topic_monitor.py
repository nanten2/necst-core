#! /usr/bin/env python3

name = 'topic_monitor'

# ----
import threading

import rospy
import time
import std_msgs.msg

class topic_monitor(object):

    def __init__(self):
        self.topic_dic = {} #[{topic:,data:,time:,}]
        self.th = threading.Thread(target= self.loop)
        self.th.start()
        print("tmmonitor")
        pass


    def regist(self, data):
        #data = {'topic': arg,'time': time.time(), 'msgs': {'data': req.data}}
        self.topic_dic[data["topic"]] = data["msgs"]["data"]
        return

    def loop(self):
        while not rospy.is_shutdown():
            print("------------------")
            for l in list(self.topic_dic):
                time.sleep(0.1)
                data = self.topic_dic[l]
                print(l+" : %s"%(data))
                #self.data_list.remove(dic)
            else:
                pass
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
