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
        if topic_name not in self.pub:
            self.pub[topic_name] = rospy.Publisher(name = topic_name, data_class = data_class, queue_size = 1, latch = False)
            time.sleep(0.01)
            pass
        return


class logger(object):

    def __init__(self):
        self.make_pub = make_pub()

    def start(self, db_path):
        topic_name = '/logger_path'
        data_class = std_msgs.msg.String

        self.make_pub.publish(topic_name, data_class, msg = db_path)
        return

    def stop(self):
        topic_name = '/logger_path'
        data_class = std_msgs.msg.String

        self.make_pub.publish(topic_name, data_class, msg = '')
        return


class test(object):

    def __init__(self):
        self.make_pub = make_pub()

    def msg_test(self, db_path):
        topic_name = '/test_topic'
        data_class = std_msgs.msg.Float64

        self.make_pub.publish(topic_name, data_class, msg = db_path)
        return
