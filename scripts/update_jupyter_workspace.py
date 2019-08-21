#!/usr/bin/env python3

import time
import pathlib
import shutil
import rospy

if __name__ == '__main__':
    rospy.init_node('update_jupyter_workspace')

    path = pathlib.Path.home()
    data_paths = sorted((path/'data').glob('**/*.necstdb'))

    while not rospy.is_shutdown():
        for db_path in data_paths:
            db_name = 'result.necstdb'
            relative_path = db_path.relative_to(path/'data')
            jupyter_path = (path/'jupyter'/relative_path.with_suffix(''))

            if jupyter_path.exists(): continue

            jupyter_path.mkdir(parents=True)
            (jupyter_path/db_name).symlink_to(db_path.relative_to(jupyter_path))

            tmp = jupyter_path.parent
            while tmp.name != '':

                if (tmp/'template').exists():
                    for _f in (tmp/'template').glob('*.ipynb'):
                        shutil.copy(str(_f), str(jupyter_path))
                        continue
                    break

                tmp = tmp.parent
                continue

            continue

        time.sleep(10)
        continue
