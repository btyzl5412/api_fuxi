"""
======================================
Author:包天宇
Time:2021-04-23 21:29
E-mail:uattb991492@icccuat.com
======================================
"""
import os
from common.handle_path import CONF_DIR
from configparser import ConfigParser


class Conf(ConfigParser):

    def __init__(self, filename):
        # 重写类方法
        super().__init__()
        self.read(filename, encoding='utf-8')


conf = Conf(filename=os.path.join(CONF_DIR,'conf.ini'))
