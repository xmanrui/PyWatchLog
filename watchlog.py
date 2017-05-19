# -*- coding: utf-8 -*-

from watchdog.events import *
import os


class LogFileEventHandler(FileSystemEventHandler):
    def __init__(self, log_filename):
        FileSystemEventHandler.__init__(self)
        self.log_filename = log_filename
        texts = self.read_log_file()
        self.line_num = len(texts)

    def read_log_file(self):
        with open(self.log_filename, 'r') as f:
            all_the_text = f.readlines()
        return all_the_text

    def on_modified(self, event):
        '''
        一次修改log_filename文件会调用三次on_modified，每次的event.src_path都不一样，类似:
        ./log\mylog.log___jb_tmp___
        ./log\mylog.log___jb_old___
        ./log\mylog.log
        前两次会加上后缀，此时mylog.log不可访问，第三次才可以，所以要判断event.src_path和self.log_filename，
        不相等则退出本函数。
        '''

        if os.path.abspath(event.src_path) != os.path.abspath(self.log_filename):
            return

        all_the_text = self.read_log_file()
        line_num = len(all_the_text)
        if line_num != self.line_num:
            offset = line_num - self.line_num
            if offset > 0:
                for i in range(offset):
                    print(all_the_text[self.line_num + i].rstrip('\n'))
            self.line_num = line_num

        print('*' * 80)

