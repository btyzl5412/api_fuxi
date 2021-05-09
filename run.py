"""
======================================
Author:包天宇
Time:2021-05-09 15:51
E-mail:uattb991492@icccuat.com
======================================
"""
import unittest
from unittestreport import TestRunner
from common.handle_path import TEST_DIR
from common.handle_path import REPORT_DIR

# 用例加载
su = unittest.defaultTestLoader.discover(TEST_DIR)
runner = TestRunner(su, report_dir=REPORT_DIR,
                    title='接口自动化测试报告',
                    tester='bty',
                    desc="接口复习")
# 运行用例
runner.run()

# 用例执行完成后，发送报告邮件
runner.send_email(host='smtp.163.com',
                  port=994,
                  user='btycly5412@163.com',
                  password='IPFSQEOKXXORGPPR',
                  to_addrs='717584959@qq.com',
                  is_file=True)
