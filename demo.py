# -*- coding: utf-8 -*-

import watchlog
from watchdog.observers import Observer
import time
import multiprocessing


def run_watch_log(log_dir, log_file):
    print('run watchlog...')
    observer = Observer()
    event_handler = watchlog.LogFileEventHandler(log_file)
    observer.schedule(event_handler, log_dir, True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print('end watchlog!!!')


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
    log_file = './log/demo.log'
    log_dir = './log'
    p1 = multiprocessing.Process(target=run_watch_log, args=(log_dir, log_file))
    p2 = multiprocessing.Process(target=generate_log, args=(log_file, ))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

