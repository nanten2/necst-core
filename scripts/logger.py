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

#def update_topic_list(last_topic_list, new_topic_list):
#    if last_topic_list == new_topic_list: topic_list = new_topic_list
#    else:

def callback(req, arg):
    data = {'topic': arg,'time': time.time(), 'msgs': {'data': req.data}}
    #'msgs': {'data': req.data,'time': req.timestamp}
    for f in funclist.func_li:
        f(data)
    return

def start_thread():
    th = threading.Thread(target = make_topic_list)
    th.setDeamon(True)
    th.start()

if __name__ == '__main__':
    rospy.init_node(name)
    
    start_thread()

    msgtype_dict = {'std_msgs/Int32': std_msgs.msg.Int32,
                    'std_msgs/Float64': std_msgs.msg.Float64}
    
    topic_form = [
       rospy.Subscriber(
          name = topic_li[i][0],
          data = msgtype_dict[topic_li[i][0]],
          callback = callback,
          callback_args = topic_li[i][0],
          queue_size = 1
       ) for i in range(len(topic_li))
    ]

    rospy.spin()
