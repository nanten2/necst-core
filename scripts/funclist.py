#!/usr/bin/env python3

from typing import List
from collections.abc import Callable

# from . import db_logger_operation
import db_logger_always

# from . import topic_monitor
# import web_monitor

# db_logger_operation = db_logger_operation.db_logger_operation()
db_logger_always = db_logger_always.db_logger_always()
# topic_monitor = topic_monitor.topic_monitor()
# web_monitor = web_monitor.web_monitor()


def func_li() -> List[Callable]:
    func_list = [
        # db_logger_operation.regist,
        db_logger_always.regist,
        # topic_monitor.regist,
        # web_monitor.web_monitor.regist,
    ]
    return func_list
