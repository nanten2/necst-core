#!/usr/bin/env python3

name = 'pc_status'


import psutil

import rospy
import std_msgs.msg


if __name__ == '__main__':
    rospy.init_node(name)
    rate_ = rospy.get_param('~rate', 0.1)
    rate = rospy.Rate(rate_)
    
    cpu = rospy.Publisher(name+'/cpu', std_msgs.msg.Float32, queue_size=1, latch=True)
    mem = rospy.Publisher(name+'/mem', std_msgs.msg.Float32, queue_size=1, latch=True)
    disk = rospy.Publisher(name+'/disk', std_msgs.msg.Float32, queue_size=1, latch=True)
    login = rospy.Publisher(name+'/login', std_msgs.msg.Int16, queue_size=1, latch=True)
    proc = rospy.Publisher(name+'/proc', std_msgs.msg.Int16, queue_size=1, latch=True)
    
    def publish_if_changed(pub, last, new):
        if new != last:
            pub.publish(new)
            pass
        return new
    
    last = {'cpu': None, 'mem': None, 'disk': None, 'login': None, 'proc': None}
    while not rospy.is_shutdown():
        last['cpu'] = publish_if_changed(cpu, last['cpu'], psutil.cpu_percent())
        last['mem'] = publish_if_changed(mem, last['mem'], psutil.virtual_memory().percent)
        last['disk'] = publish_if_changed(disk, last['disk'], psutil.disk_usage('/').percent)
        last['login'] = publish_if_changed(login, last['login'], len(psutil.users()))
        last['proc'] = publish_if_changed(proc, last['proc'], len(psutil.pids()))
        rate.sleep()
        continue
