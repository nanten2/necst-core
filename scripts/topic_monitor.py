#! /usr/bin/env python3

name = 'topic_monitor'

# ----
import threading

import rospy
import std_msgs.msg

class topic_monitor(object):

    def __init__(self):
        self.data_list = [] #[{topic:,data:,time:,}]
        self.th = threading.Thread(target= self.loop)
        self.th.start()
        print("tmmonitor")
        pass


    def regist(self, data):
        self.data_list.append(data)
        return

    def loop(self):
        while not rospy.is_shutdown():
            num = len(self.data_list)
            for i in range(num):
                print("------------------")
                dic = self.data_list[i]
                topic = dic["topic"]
                data = dic["data"]
                print(topic+" : %s"%(data))

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
