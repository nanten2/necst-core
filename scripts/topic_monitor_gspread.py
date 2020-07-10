#! /usr/bin/env python3

name = 'topic_monitor_gspread'

# ----
import threading
import datetime
import rospy
import time
import std_msgs.msg
import gspread
import json

from oauth2client.service_account import ServiceAccountCredentials


class topic_monitor_gspread(object):

    def __init__(self):

        json = "/home/telescopio/ros/src/necst-sisrx_b67/lib/double-runway-282511-758acb947e09.json"
        spread_sheet_key = "1eQLqUqIzj32dqqfcpFc5-DMvGDqL7Nt7jnGnZk8stTk"
        self.ws = self.connect_gspread(json,spread_sheet_key)

        rospy.Subscriber("/dev/218/ip_192_168_100_45/temp/ch1",std_msgs.msg.Float64,self.dewar_temp,callback_args=1)
        rospy.Subscriber("/dev/218/ip_192_168_100_45/temp/ch2",std_msgs.msg.Float64,self.dewar_temp,callback_args=2)
        rospy.Subscriber("/dev/218/ip_192_168_100_45/temp/ch3",std_msgs.msg.Float64,self.dewar_temp,callback_args=3)
        rospy.Subscriber("/dev/218/ip_192_168_100_45/temp/ch4",std_msgs.msg.Float64,self.dewar_temp,callback_args=4)
        rospy.Subscriber("/dev/tpg/ip_192_168_100_178/pressure",std_msgs.msg.Float64,self.dewar_press)


        self.dewar_tmp = {}

        self.dewar_pressure = None
        self.dewar_tmp[1] = None
        self.dewar_tmp[2] = None
        self.dewar_tmp[3] = None
        self.dewar_tmp[4] = None
        self.update_t = None

        pass

    def dewar_temp(self, q, ch):
        self.dewar_tmp[ch] = q.data
        t = datetime.datetime.now()
        self.update_t = t.strftime("%Y/%m/%d-%H:%M:%S")
        return

    def dewar_press(self, q,):
        self.dewar_pressure = q.data
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


            ds = self.ws.range('A1:K15')

            #dewar pressure
            ds[8].value = self.dewar_pressure

            #dewar tmp
            #ds[4].value = self.dewar_tmp[1]
            #ds[5].value = self.dewar_tmp[2]
            #ds[6].value = self.dewar_tmp[3]
            #ds[7].value = self.dewar_tmp[4]
            #self.ws.update_cell(9,  7 , self.dewar_tmp[1])
            #self.ws.update_cell(10, 7 , self.dewar_tmp[2])
            #self.ws.update_cell(11, 7 , self.dewar_tmp[3])
            #self.ws.update_cell(12, 7 , self.dewar_tmp[4])
            #ds[8].value = self.update_t

            self.ws.update_cells(ds)

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
