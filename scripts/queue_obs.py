#! /usr/bin/env python3

name = 'queue_obs'

import time
import datetime
import threading
import pandas
import subprocess
import gspread
import json
import rospy
from oauth2client.service_account import ServiceAccountCredentials

class queue_observation(object):
    def __init__(self):
        self.jsonf = "/home/exito/ros/src/necst-1p85m2019/lib/observation-queue-1471de721edb.json"
        self.spread_sheet_key = "175mbsv16ESc0-DXGVpR1X7x-0QOCHwnRfLgrvU8PAOQ"
        self.obs_path = '/home/exito/ros/src/necst-1p85m2019/observation/'

    def connect_gspread(self,jsonf,key,sheet=None):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
        gc = gspread.authorize(credentials)
        SPREADSHEET_KEY = key

        if sheet ==None:
            worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
        elif type(sheet) == str:
            worksheet = gc.open_by_key(SPREADSHEET_KEY).worksheet(sheet)
        return worksheet

    def queue_execute(self,ws):
        pd = pandas.DataFrame(ws.get_all_values())
        if len(pd) <= 1:
            return
        t= pd.loc[1][0].split('/')
        unixtime = datetime.datetime(int(t[0]),int(t[1]),int(t[2]),int(t[3]),int(t[4]),tzinfo=datetime.timezone.utc).timestamp()
        order = pd.loc[1][1]
        # error date
        if time.time() - unixtime >= 3600:
            ws2 = self.connect_gspread(self.jsonf,self.spread_sheet_key,sheet='error order')
            pd2 = pandas.DataFrame(ws2.get_all_values())
            pd2 = pd2.append(pd.loc[1])
            self.update_worksheet(ws2,pd2)
            print('error order: '+str(t)+order)
            ws.delete_rows(2)
        #execute obs
        elif time.time() >= unixtime:
            print(str(datetime.datetime.now())+':start ' +order)
            self.execute_obs(order)
            print(str(datetime.datetime.now())+':end ' +order)
            ws.delete_rows(2)
        else:
            pass
        return

    def execute_obs(self,filename):
        cmd = ['ipython',self.obs_path+filename]
        proc= subprocess.run(cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True)
        print(proc.stdout)
        return

    def toAlpha(self,num):
        if num<=26:
            return chr(64+num)
        elif num%26==0:
            return toAlpha(num//26-1)+chr(90)
        else:
            return toAlpha(num//26)+chr(64+num%26)

    def update_worksheet(self,ws,pd):
        col_lastnum = len(pd.columns) # DataFrameの列数
        row_lastnum = len(pd.index)   # DataFrameの行数

        cell_list = ws.range('A1:'+self.toAlpha(col_lastnum)+str(row_lastnum))
        for cell in cell_list:
            val = pd.iloc[cell.row-1][cell.col-1]
            cell.value = val
        ws.update_cells(cell_list)
        return

    def queue_obs(self):
        while not rospy.is_shutdown():
            ws = self.connect_gspread(self.jsonf,self.spread_sheet_key)
            self.queue_execute(ws)
            time.sleep(60)
            continue
        return

    def start_thread(self):
        th = threading.Thread(target = self.queue_obs)
        th.setDaemon(True)
        th.start()

if __name__ == '__main__':
    rospy.init_node(name)
    queue_obs = queue_observation()
    queue_obs.start_thread()
    rospy.spin()
