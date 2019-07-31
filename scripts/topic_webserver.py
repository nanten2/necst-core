#!/usr/bin/env python3

import rospy, os, ssl
from http.server import HTTPServer, SimpleHTTPRequestHandler

def kill():
    os.system("kill -KILL " + str(os.getpid()))

os.chdir("/home/exito/ros/src/necst-core/web_monitor")
host = 'localhost'
port = 10000
httpd = HTTPServer(("", port), SimpleHTTPRequestHandler)
print("serving at port", port)
httpd.serve_forever()

rospy.init_node("webserver")
rospy.on_shutdown(kill)
