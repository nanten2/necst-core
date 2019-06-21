#!/usr/bin/env python3

name = 'logger'

print("a")
import time
import threading
print("b")
import funclist
print("c")

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
    print("4")
    while not rospy.is_shutdown():
        new_topic_li = make_topic_list()
        global topic_li
        if topic_li == new_topic_li:
            pass

        elif topic_li >= new_topic_li:
            topic_li = new_topic_li
            print("5")
            make_Subscriber()
            print(topic_li)
            print("make sub")
        """
        elif topic_li < new_topic_li:
            topic_li = new_topic_li
            dec_Subscriber()
        """

def make_Subscriber():
    print("6")
    global topic_li
    for i in range(len(topic_li)):
        print("7")
        rospy.Subscriber(
            name = topic_li[i][0],
            data_class = msgtype_dict[topic_li[i][1]],
            callback = callback,
            callback_args = topic_li[i][0],
            queue_size = 1)
        print("8")
"""
def dec_Subscriber():
    global topic_li
    for i in range(len(topic_li)):
        rospy.Subscriber(
            name = topic_li[i][0],
            data_class = msgtype_dict[topic_li[i][1]],
            callback = callback2,
            callback_args = topic_li[i][0],
            queue_size = 1)
"""
def callback(req, arg):
    print("9")
    data = {'topic': arg,'time': time.time(), 'msgs': {'data': req.data}}
    #'msgs': {'data': req.data,'time': req.timestamp}
    flist = funclist.func_li()
    for f in flist:
        f(data)
    print("10")
    return
"""
def callback2(req, arg):
    data = {'topic': arg,'time': time.time(), 'msgs': {'data': req.data}}
    #'msgs': {'data': req.data,'time': req.timestamp}
    flist2 = funclist.func_li2()
    for f in flist:
        f(data)
    return
"""

def start_thread():
    print("3")
    th = threading.Thread(target = compare_topic_list)
    th.setDaemon(True)
    th.start()

if __name__ == '__main__':
    print("d")
    rospy.init_node(name)
    print("1")
    topic_li = []
    start_thread()
    print("2")

    msgtype_dict = {'std_msgs/Int32': std_msgs.msg.Int32,
                    'std_msgs/Float64': std_msgs.msg.Float64}
    rospy.spin()
