# -*- coding: utf-8 -*-

import watchlog
import time
import multiprocessing
import os


def generate_log(log_path):
    print('run generate_log....')
    while True:
        time.sleep(0.5)
        with open(log_path, 'a') as fh:
            for i in range(10):
                msg = time.strftime('test msg: %Y-%m-%d %H:%M:%S\n', time.localtime())
                fh.writelines(msg)
                fh.flush()


if __name__ == '__main__':
    log_file = 'demo.log'
    log_dir = './log'
    log_file_path = os.path.join(log_dir, log_file)
    p1 = multiprocessing.Process(target=watchlog.run_watch_log, args=(log_dir, log_file))
    p2 = multiprocessing.Process(target=generate_log, args=(log_file_path, ))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

