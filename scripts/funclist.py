#!usr/bin/env python3

import db_logger_operation
import topic_monitor

class funclist(self):
    
    def __init__(self):

        self.db_logger_operation = db_logger_operation.db_logger_operation()
        self.topic_monitor = topic_monitor.topic_monitor()
 
    def funcli(self, data):
        funcli =[self.db_logger_operation.regist(data),
                 self.topic_monitor.regist(data)]
        return funcli

