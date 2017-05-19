# -*- coding: utf-8 -*-

import watchlog
from watchdog.observers import Observer
import time


def run_watchlog(logdir, logfile):
    print('run watchlog...')
    observer = Observer()
    event_handler = watchlog.LogFileEventHandler(logfile)
    observer.schedule(event_handler, logdir, True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print('end watchlog!!!')

if __name__ == '__main__':
    logfile = './log/demo.log'
    logdir = './log'
    run_watchlog(logdir, logfile)

