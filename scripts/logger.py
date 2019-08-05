#!/usr/bin/env python3

name = 'logger'

import time
import funclist

import rospy
import std_msgs.msg

ignores = [
    '/rosout',
    '/rosout_agg',
]

def get_current_topic_list():
    topic_list = rospy.get_published_topics()
    for topic in topic_list[:]:
        if topic[0] in ignores:
            topic_list.remove(topic)
            pass
        continue
    return topic_list

def make_subscriber(topic):
    topic_name = topic[0]
    topic_type = eval(topic[1].replace('/', '.msg.'))
    rospy.Subscriber(
        name = topic_name,
        data_class = topic_type,
        callback = callback,
        callback_args = topic_name,
        queue_size = 1
    )

def callback(req, arg):
    keys = [attr for attr in req.__dir__() 
            if not attr.startswith('_') 
            and not attr in ['serialize', 'deserialize
                             'serialize_numpy', 'deserialize_numpy']]
    msg_dict = {key: req.__getattribute__(key) for key in keys}
    
    data = {'topic': arg,'time': time.time(), 'msgs': msg_dict, 'req': req}
    
    flist = funclist.func_li()
    for f in flist:
        f(data)
    return


if __name__ == '__main__':
    rospy.init_node(name)
    
    subscribing_topic_list = []
    while not rospy.is_shutdown():
        current_topic_list = get_current_topic_list()
        for topic in current_topic_list:
            if topic not in subscribing_topic_list:
                make_subscriber(topic)
                subscribing_topic_list.append(topic)
                pass
            continue
        time.sleep(1)
        continue
