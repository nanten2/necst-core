#!usr/bin/env python3

name  = 'db_logger_operation'

import time
import threading
import necstdb
import pathlib

import rospy
import std_msgs.msg

class db_logger_operation(object):

    def __init__(self):
        self.data_list = []
        self.table_dict = {}
        self.db_dir = pathlib.Path.home() / 'data/operation'
        self.db_path = ''
        t1 = time.time()
        self.sub_path = rospy.Subscriber(
            name = '/logger_path',
            data_class = std_msgs.msg.String,
            callback = self.callback_path,
            queue_size = 1,
        )

        self.th = threading.Thread(target= self.loop)
        self.th.start()
        pass

    def callback_path(self, req):
        if req.data != '':
            self.db_path = ''
            self.data_list = []
            self.close_tables()
            self.db = necstdb.opendb(self.db_dir / req.data, mode = 'w')
            self.db_path = req.data
            time.sleep(0.1)

        else:
            self.db_path = req.data
            pass
        return

    def close_tables(self):
        tables = self.table_dict
        self.table_dict = {}
        [tables[name].close() for name in tables]
        return

    def regist(self, data):
        if self.db_path != '':
            self.data_list.append(data)
            pass
        return

    def loop(self):

        while True:
            if len(self.data_list) ==0:
                self.close_tables()
                if rospy.is_shutdown():
                    break
                time.sleep(0.01)
                continue

            d = self.data_list.pop(0)

            table_name = d['topic'].replace('/', '-').strip('-')
            table_data = [d['received_time']]
            table_info = [{'key': 'timestamp',
                           'format': 'd',
                           'size': 8}]

            for slot in d['slots']:

                if slot['type'].startswith('bool'):
                    slot['value'] = int(slot['value'])
                    info = {'format': 'i', 'size': 4}


                elif slot['type'].startswith('byte'):
                    info = {'format': '{0}s'.format(len(slot['value'])), 'size': len(slot['value'])}

                elif slot['type'].startswith('char[]'):
                    continue

                elif slot['type'].startswith('char'):
                    info = {'format': 'c', 'size': 1}
                    if isinstance(slot['value'], str):
                        slot['value'] = slot['value'].encode()
                        pass

                elif slot['type'].startswith('float32'):
                    info = {'format': 'f', 'size': 4}

                elif slot['type'].startswith('float64'):
                    info = {'format': 'd', 'size': 8}

                elif slot['type'].startswith('int8'):
                    info = {'format': 'b', 'size': 1}

                elif slot['type'].startswith('int16'):
                    info = {'format': 'h', 'size': 2}

                elif slot['type'].startswith('int32'):
                    info = {'format': 'i', 'size': 4}

                elif slot['type'].startswith('int64'):
                    info = {'format': 'q', 'size': 8}

                elif slot['type'].startswith('string[]'):
                    continue

                elif slot['type'].startswith('string'):
                    info = {'format': '{0}s'.format(len(slot['value'])), 'size': len(slot['value'])}
                    if len(slot['value'])%4 == 0:
                        str_size = len(slot['value'])
                    else:
                        str_size = len(slot['value']) + (4-len(slot['value'])%4)

                    info = {'format': '{0}s'.format(str_size), 'size': str_size}
                    if isinstance(slot['value'], str):
                        slot['value'] = slot['value'].encode()
                        pass

                elif slot['type'].startswith('uint8'):
                    info = {'format': 'B', 'size': 1}

                elif slot['type'].startswith('unit16'):
                    info = {'format': 'H', 'size': 2}

                elif slot['type'].startswith('unit32'):
                    info = {'format': 'I', 'size': 4}

                elif slot['type'].startswith('unit64'):
                    info = {'format': 'Q', 'size': 8}
                else:
                    continue

                if isinstance(slot['value'], tuple):
                    # for MultiArray
                    dlen = len(slot['value'])
                    info['format'] = '{0:d}{1:s}'.format(dlen, info['format'])
                    info['size'] *= dlen
                    table_data += slot['value']
                else:
                    table_data += [slot['value']]
                    pass

                info['key'] = slot['key']
                table_info.append(info)


            if table_name not in self.table_dict:
                self.db.create_table(table_name,
                            {'data': table_info,
                             'memo': 'generated by db_logger_operation',
                             'version': necstdb.__version__,})

                self.table_dict[table_name] = self.db.open_table(table_name, mode='ab')
                pass


            self.table_dict[table_name].append(*table_data)
            continue
        return
