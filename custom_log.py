# -*- coding: utf-8 -*-

import logging
import threading
import os

Lock = threading.Lock()


def make_dir(dir_path):
    if os.path.exists(dir_path):
        return False
    else:
        os.makedirs(dir_path)
    return True


def make_file(filepath):
    thedir, filename = os.path.split(filepath)
    if not thedir or not filename:
        return False

    if not os.path.exists(filepath):
        make_dir(thedir)
        fh = open(filepath, 'w')
        fh.close()
        return True
    else:
        return False


class SettingLogSingleton(object):
    '''
    log只能初始化一次，否则写log会重复，所以才使用单例模式
    '''
    # 定义静态变量实例
    __instance = None
    __log_dir = ''
    __log_file = ''

    @classmethod
    def add_message_to_setting_log(cls, msg):
        logger = logging.getLogger(cls.__log_file)
        logger.debug(msg)

    @classmethod
    def __init_logger(cls):
        setting_log_filename = cls.__log_file
        make_file(setting_log_filename)
        logger = logging.getLogger(setting_log_filename)
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(setting_log_filename)
        fh.setLevel(logging.DEBUG)
        fm = 'setting_log: %(levelname)s: [%(filename)s line:%(lineno)d %(funcName)s] -- [%(asctime)s]  %(message)s'
        formatter = logging.Formatter(fm)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    def __new__(cls, watch_dir, filename):
        cls.__log_dir = watch_dir
        cls.__log_file = os.path.join(watch_dir, filename)
        if not cls.__instance:
            try:
                Lock.acquire()
                # double check
                if not cls.__instance:
                    # cls.__instance = super(SettingLogSingleton, cls).__new__(cls, *args, **kwargs)
                    cls.__instance = object.__new__(cls)
                    cls.__instance.__init_logger()
                    cls.__instance.__init_logger()
                    cls.__instance.__init_logger()

            finally:
                Lock.release()
        return cls.__instance


def test_singleton():
    import time
    log_dir = './log'
    log_file = 'demo.log'
    obj2 = SettingLogSingleton(log_dir, log_file)
    obj = SettingLogSingleton(log_dir, log_file)
    print(id(obj))
    obj.add_message_to_setting_log('*' * 80)
    obj = SettingLogSingleton(log_dir, log_file)
    print(id(obj))
    obj.add_message_to_setting_log('for testing')
    obj = SettingLogSingleton(log_dir, log_file)
    obj.add_message_to_setting_log('for testing')
    obj.add_message_to_setting_log('for testing')
    print(id(obj))


if __name__ == "__main__":
    test_singleton()



