# coding = utf-8
import configparser
import os
from threading import Lock
import time


def get_value(section, item):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), r'config\config.ini')
    conf = configparser.ConfigParser()
    conf.read(file_path, encoding='utf-8')
    value = conf.get(section, item)
    return value


lock = Lock()


def write_value(section, item, value):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), r'config\config.ini')
    conf = configparser.ConfigParser()
    conf.read(file_path, encoding='utf-8')
    conf.set(section, item, value)
    lock.acquire()
    time.sleep(10)
    try:
        conf.write(open(file_path, 'w', encoding='utf-8'))
    finally:
        lock.release()


if __name__ == '__main__':
    get_value('login', 'username')
    write_value('token', 'token', '1234567890')

