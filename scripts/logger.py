#!/usr/bin/env python3

from typing import List, Tuple, Union
import time

import rospy
import std_msgs.msg
import necst.msg

import funclist

node_name = "logger"

IGNORE_TOPICS = [
    "/rosout",
    "/rosout_agg",
]
IGNORE_TYPES = [
    "unknown type",
]

ROSMsg = Union[std_msgs.msg, necst.msg]


def get_current_topic_list() -> List[Tuple[str, str]]:
    topic_list = rospy.get_published_topics()
    for topic in topic_list:
        if topic[0] in IGNORE_TOPICS:
            topic_list.remove(topic)
        elif topic[1] in IGNORE_TYPES:
            topic_list.remove(topic)
            pass
        continue
    return topic_list


def make_subscriber(topic: Tuple[str, str]) -> None:
    topic_name = topic[0]
    topic_type = eval(topic[1].replace("/", ".msg."))
    rospy.Subscriber(
        name=topic_name,
        data_class=topic_type,
        callback=record,
        callback_args=topic_name,
        queue_size=1,
    )


def record(req: ROSMsg, arg: str) -> None:
    slots = [
        {"key": key, "type": type_, "value": req.__getattribute__(key)}
        for key, type_ in zip(req.__slots__, req._slot_types)
    ]

    data = {"topic": arg, "received_time": time.time(), "slots": slots}

    flist = funclist.func_li()
    for f in flist:
        f(data)
    return


if __name__ == "__main__":
    rospy.init_node(node_name)

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
