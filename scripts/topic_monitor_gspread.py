#! /usr/bin/env python3

name = 'topic_monitor_gspread'

# ----
import threading

import rospy
import time
import std_msgs.msg
import gspread
import json

from oauth2client.service_account import ServiceAccountCredentials


class topic_monitor_gspread(object):


    json = ""
    spread_sheet_key = ""
    ws = regist_gspread(json,spread_sheet_key)

    def __init__(self):

        rospy.Subscriber("/dev/218/ip_192_168_100_45/temp/ch1",std_msgs.msg.Float64,self.dewar_temp,callback_args=1)
        rospy.Subscriber("/dev/218/ip_192_168_100_45/temp/ch2",std_msgs.msg.Float64,self.dewar_temp,callback_args=2)
        rospy.Subscriber("/dev/218/ip_192_168_100_45/temp/ch3",std_msgs.msg.Float64,self.dewar_temp,callback_args=3)
        rospy.Subscriber("/dev/218/ip_192_168_100_45/temp/ch4",std_msgs.msg.Float64,self.dewar_temp,callback_args=4)

        self.dewar_tmp = {}

        pass

    def dewar_temp(self, q, ch):
        self.dewar_tmp[ch] = q.data
        return

    def connect_gspread(self,json,key):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json, scope)
        gc = gspread.authorize(credentials)
        SPREADSHEET_KEY = key
        worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
        return worksheet

    def regist_gspread(self):
        while not rospy.is_shutdown():

            #dewar tmp
            self.ws.update_cell(7,9, self.dewar_tmp[1])
            self.ws.update_cell(7,10, self.dewar_tmp[2])
            self.ws.update_cell(7,11, self.dewar_tmp[3])
            self.ws.update_cell(7,12, self.dewar_tmp[4])

            time.sleep(3)


            continue
        return


    def thread(self):
        th = threading.Thread(target=self.regist_gspread)
        th.setDaemon(True)
        th.start()


if __name__=='__main__':
    rospy.init_node(name)
    tm = topic_monitor_gspread()
    tm.thread()
    rospy.spin()
