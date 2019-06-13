#!/usr/bin/env python3

name = 'topic_monitor'

import sys
import time
import datetime
import threading
import rospy
import std_msgs.msg

class topic_monitor(object):

    def __init__(self):
        self.msgtype_dict = {'std_msgs/String': std_msgs.msg.String,
                             'std_msgs/Float64': std_msgs.msg.Float64}
        self.values = {}
        self.refreshing = False
        _topic_li = rospy.get_published_topics()
        self.topic_li = []
        for i in range(len(_topic_li)):
            if _topic_li[i][0] == '/rosout': pass
            elif _topic_li[i][0] == '/rosout_agg': pass
            elif _topic_li[i][0] == '/test/revolution': pass
            else: self.topic_li.append(_topic_li[i])

    def callback(self, msg, args):
        self.values[args['name']] = msg.data
        self.refresh()
        return

    def refresh(self):
        while self.refreshing == True:
            time.sleep(0.1)
            continue
        
        self.refreshing = True
        maxlen = max([len(_k) for _k in self.values.keys()])
        print('----')
        for key in sorted(self.values):
            print(('{0:<'+str(maxlen)+'} {1}').format(key, self.values[key]))
            continue
        self.refreshing = False
        return

if __name__ == '__main__':
    rospy.init_node(name)
    tm = topic_monitor()

    topic_from = [rospy.Subscriber(
                name = tm.topic_li[i][0],
                data_class = tm.msgtype_dict[tm.topic_li[i][1]],
                callback = tm.callback,
                callback_args = {'name': i },
                queue_size = 1,
            ) for i in range(len(tm.topic_li))]

    rospy.spin()
