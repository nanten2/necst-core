#!usr/bin/env python3

import db_logger_operation
import topic_monitor
import db_logger_always
#import db_logger_always_vol2
#import web_monitor

db_logger_operation = db_logger_operation.db_logger_operation()
topic_monitor = topic_monitor.topic_monitor()
db_logger_always = db_logger_always.db_logger_always()
#db_logger_always_vol2 = db_logger_always_vol2.db_logger_always_vol2()

#web_monitor = web_monitor.web_monitor()

def func_li():
    func_li = [db_logger_operation.regist,
               topic_monitor.regist,
               db_logger_always.regist,
               #db_logger_always_vol2.regist,
               #web_monitor.web_monitor.regist,
               ]
    return func_li
