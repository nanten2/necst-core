#!/usr/bin/env python3

import rospy
import numpy as np
import time
from std_msgs.msg import Int32
from std_msgs.msg import Float64


def reader():
    rospy.init_node("e8257d_trigger")
    name_list = []
    for band in ["100ghz", "200ghz"]:
        for stage in ["1st", "2nd_upper", "2nd_lower"]:
            name = f"sg_{band}_{stage}"
            name_list.append(name)

    pub_freq_list = []
    pub_power_list = []
    pub_onoff_list = []

    for name in name_list:
        pub_freq = rospy.Publisher(f"{name}_freq_cmd", Float64, queue_size=1)
        pub_power = rospy.Publisher(f"{name}_power_cmd", Float64, queue_size=1)
        pub_onoff = rospy.Publisher(f"{name}_onoff_cmd", Int32, queue_size=1)
        pub_freq_list.append(pub_freq)
        pub_power_list.append(pub_power)
        pub_onoff_list.append(pub_onoff)

    while not rospy.is_shutdown():

        msg_freq = Float64(np.nan)
        msg_power = Float64(np.nan)
        msg_onoff = Int32(-1)

        [publisher.publish(msg_freq) for publisher in pub_freq_list]
        time.sleep(2)
        [publisher.publish(msg_power) for publisher in pub_power_list]
        time.sleep(2)
        [publisher.publish(msg_onoff) for publisher in pub_onoff_list]
        time.sleep(2)


if __name__ == "__main__":
    reader()
