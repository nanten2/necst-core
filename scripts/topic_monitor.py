#! /usr/bin/env python3

name = 'topic_monitor'

# ----
import threading

import rospy
import time
import std_msgs.msg

class topic_monitor(object):

    def __init__(self):
        self.topic_dict = {} #{'topic1':data1,'topic2':data2, ...}
        self.th = threading.Thread(target= self.loop)
        self.th.start()
        pass


    def regist(self, data):
        #data = {'topic': arg,'received_time': time.time(), 'slots': [{'key': key,'type', type,'value': req.data}]}
        self.topic_dict[data['topic']] = data
        return

    def loop(self):
        while not rospy.is_shutdown():
            print("------------------")

            for topic, data in sorted(self.topic_dict.items()):
                for slot in data['slots']:
                    if isinstance(slot['value'], tuple):
                        continue
                    if slot['key'] == 'layout':
                        continue
                    if time.time() - data['received_time'] > 10:
                        continue
                    if slot['key'] == 'data':
                        print(topic+" : %s"%(slot['value']))
                    else:
                        print(topic+"."+slot['key']+" : %s"%(slot['value']))
                    continue
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
