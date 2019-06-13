#!/usr/bin/env python3

node_name = 'core_controller'

import rospy

import time
import std_msgs.msg


class controller(object):

    def __init__(self):
        self.ps = PS()
        self.logger = LOGGER()


class PS(object):

    def __init__(self):
        self.pub = {}
        pass

    def publish(self, topic_name, msg):
        self.pub[topic_name].publish(msg)
        return

    def set_publish(self, topic_name, data_class, queue_size, latch = True):
        if topic_name not in self.pub:
            self.pub[topic_name] = rospy.Publisher(name = topic_name, data_class = data_class, queue_size = queue_size, latch = latch)
            time.sleep(0.01)

        else:
            pass
        return


class LOGGER(object):

    def __init__(self):
        rospy.init_node(node_name)
        self.ps = PS()

    def start(self, db_path):
        topic_name = '/logger_path'

        self.ps.set_publish(topic_name = topic_name, data_class = std_msgs.msg.String, queue_size = 1, latch = True)

        self.ps.publish(topic_name = topic_name, msg = db_path)

    def stop(self):
        topic_name = '/logger_path'

        self.ps.set_publish(topic_name = topic_name, data_class = std_msgs.msg.String, queue_size = 1, latch = True)

        self.ps.publish(topic_name = topic_name, msg = '')
