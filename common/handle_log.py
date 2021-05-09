"""
======================================
Author:包天宇
Time:2021-04-23 20:56
E-mail:uattb991492@icccuat.com
======================================
"""
import logging
import os
from common.handle_path import LOGS_DIR
from common.handle_conf import conf


def create_log(name="my_log",level="DEBUG",sh_level="DEBUG",filename="log.log",fh_level="DEBUG"):

    # 设置日志收集器名称
    mylog = logging.getLogger(name=name)

    # 设置日志收集器等级
    mylog.setLevel(level=level)

    # 设置输出至控制台的等级
    sh = logging.StreamHandler()
    sh.setLevel(level=sh_level)

    # 将输出渠道绑定到日志收集器上
    mylog.addHandler(sh)

    # 设置输出至日志文件的等级
    fh = logging.FileHandler(filename=os.path.join(LOGS_DIR,filename),encoding="utf-8")
    fh.setLevel(level=fh_level)
    # 将输出渠道绑定到日志收集器上
    mylog.addHandler(fh)

    # 设置日志输出格式
    formats = '%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
    # 创建格式对象
    log_format = logging.Formatter(formats)

    # 设置输出到控制台的日志格式
    sh.setFormatter(log_format)
    # 设置输出到文件的日志格式
    fh.setFormatter(log_format)

    # 返回日志收集器
    return mylog


my_log = create_log(name=conf.get('logging','name'),
                    level=conf.get('logging','level'),
                    filename=conf.get('logging','filename'),
                    sh_level=conf.get('logging','sh_level'),
                    fh_level=conf.get('logging','fh_level')
                    )
