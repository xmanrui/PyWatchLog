# -*- coding: utf-8 -*-

from watchdog.events import *
import os
from watchdog.observers import Observer
import time


class LogFileEventHandler(FileSystemEventHandler):
    def __init__(self, log_filename):
        FileSystemEventHandler.__init__(self)
        self.log_filename = log_filename
        self.chunk_size = os.path.getsize(log_filename)

    def on_modified(self, event):
        """"
        一次修改log_filename文件会调用三次on_modified，每次的event.src_path都不一样，类似:
        ./log\mylog.log___jb_tmp___
        ./log\mylog.log___jb_old___
        ./log\mylog.log
        前两次会加上后缀，此时mylog.log不可访问，第三次才可以，所以要判断event.src_path和self.log_filename，
        不相等则退出本函数。
        """

        if os.path.abspath(event.src_path) != os.path.abspath(self.log_filename):
            return
        new_size = os.path.getsize(self.log_filename)
        delta_size = new_size - self.chunk_size

        if delta_size <= 0:
            self.chunk_size = new_size
            return

        with open(self.log_filename, 'r') as fh:
            fh.seek(self.chunk_size)
            data = fh.read(delta_size)
            print(data)

        self.chunk_size = new_size

        print('*' * 80)


def run_watch_log(log_dir, log_file):
    print('run watchlog...')
    file_path = os.path.join(log_dir, log_file)

    if not os.path.exists(file_path):
        raise ValueError('no such file: %s' % file_path)
        return

    observer = Observer()
    event_handler = LogFileEventHandler(file_path)
    observer.schedule(event_handler, log_dir, True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print('end watchlog!!!')

