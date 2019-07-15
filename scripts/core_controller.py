#!/usr/bin/env python3

node_name = 'core_controller'

import rospy

import time
import std_msgs.msg


class controller(object):

    def __init__(self):
        self.logger = logger()


class make_pub(object):

    def __init__(self):
        self.pub = {}
        pass

    def publish(self, topic_name, data_class, msg):
        if topic_name not in self.pub:
            self.set_publisher(topic_name = topic_name, data_class = data_class)
            pass

        self.pub[topic_name].publish(msg)
        return

    def set_publisher(self, topic_name, data_class):
        t1 = time.time()
        self.pub[topic_name] = rospy.Publisher(name = topic_name, data_class = data_class, queue_size = 1, latch = False)
        t2 = time.time()
        time.sleep(0.1)
        print("set "+str(t2-t1))
        return


class logger(object):

    def __init__(self):
        self.make_pub = make_pub()

    def start(self, db_path):
        topic_name = '/logger_path'
        data_class = std_msgs.msg.String
        t1 = time.time()
        self.make_pub.publish(topic_name, data_class, msg = db_path)
        t2 = time.time()
        print("make pub "+str(t2-t1))
        return

    def stop(self):
        topic_name = '/logger_path'
        data_class = std_msgs.msg.String

        self.make_pub.publish(topic_name, data_class, msg = '')
        return
