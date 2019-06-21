#!/usr/bin/env python3

name = 'logger'

import time
import threading
import funclist

import rospy
import std_msgs.msg

def make_topic_list():
    topic_li = []
    _topic_li = rospy.get_published_topics()
    for i in range(len(_topic_li)):
        if _topic_li[i][0] == '/rosout': pass
        elif _topic_li[i][0] == '/rosout_agg': pass
        else: topic_li.append(_topic_li[i])
    return topic_li


def compare_topic_list():
    while not rospy.is_shutdown():
        new_topic_li = make_topic_list()
        global topic_li
        if topic_li == new_topic_li:
            print("pass")
            pass

        elif topic_li != new_topic_li:
            topic_li = new_topic_li
            make_Subscriber()
            print("make sub")


def make_Subscriber():
    global topic_li
    for i in range(len(topic_li)):
        rospy.Subscriber(
            name = topic_li[i][0],
            data_class = msgtype_dict[topic_li[i][1]],
            callback = callback,
            callback_args = topic_li[i][0],
            queue_size = 1)

def callback(req, arg):
    data = {'topic': arg,'time': time.time(), 'msgs': {'data': req.data}}
    #'msgs': {'data': req.data,'time': req.timestamp}
    for f in funclist.func_li:
        f
        f(data)
    return

def start_thread():
    th = threading.Thread(target = compare_topic_list)
    th.setDaemon(True)
    th.start()

if __name__ == '__main__':
    rospy.init_node(name)

    topic_li = []
    start_thread()


    msgtype_dict = {'std_msgs/Int32': std_msgs.msg.Int32,
                    'std_msgs/Float64': std_msgs.msg.Float64}
    rospy.spin()
