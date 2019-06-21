#!usr/bin/env python3

import db_logger_operation
#import topic_monitor
#import web_monitor

db_logger_operation = db_logger_operation.db_logger_operation()
#topic_monitor = topic_monitor.topic_monitor()
#web_monitor = web_monitor.web_monitor()

func_li = [db_logger_operation.regist(data),]
           #topic_monitor.regist(data),
           #web_monitor.web_monitor.regist(data)]
