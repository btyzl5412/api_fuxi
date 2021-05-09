"""
======================================
Author:包天宇
Time:2021-04-22 23:36
E-mail:uattb991492@icccuat.com
======================================
"""
import os

# 根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配置文件目录
CONF_DIR = os.path.join(BASE_DIR,'config')

# 用例文件目录
DATA_DIR = os.path.join(BASE_DIR,'datas')

# 日志文件目录
LOGS_DIR = os.path.join(BASE_DIR,'logs')

# 报告文件目录
REPORT_DIR = os.path.join(BASE_DIR,'reports')

# 用例文件目录
TEST_DIR = os.path.join(BASE_DIR,'testcases')

if __name__ == '__main__':
    print(BASE_DIR)