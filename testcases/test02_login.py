"""
======================================
Author:包天宇
Time:2021-05-07 21:15
E-mail:uattb991492@icccuat.com
======================================
"""
import requests
import unittest
import os
import json
from common.handle_path import DATA_DIR
from common.handle_excel import Excel
from common.handle_conf import conf
from unittestreport import ddt, list_data
from common.handle_log import my_log
from common.handle_com import res_asser_expected


@ddt
class TestLogin(unittest.TestCase):
    # 准备数据（登录功能）
    # 测试用例
    excel = Excel(filename=os.path.join(DATA_DIR, 'case.xlsx'), sheetname='login')
    cases = excel.read_excel()
    # 请求头
    headers = eval(conf.get('SIT', 'headers'))
    # 基础url
    base_url = conf.get('SIT', 'base_url')

    @list_data(cases)
    def test_login(self, items):
        # url
        url = self.base_url + items['url']
        # 请求方法
        method = items['method'].lower()
        # 请求参数
        data = eval(items['data'])
        # 预期结果
        expected = eval(items['expected'])
        # id
        id = items['case_id'] + 1

        # 发起请求
        response = requests.request(method=method, url=url, json=data, headers=self.headers)
        res = response.json()

        # 进行断言
        try:
            res_asser_expected(expected, res)
        except AssertionError as e:
            my_log.error("用例--【编号为:{}，标题为:{}】---执行失败".format(items['case_id'], items['title']))
            my_log.exception(e)
            self.excel.create_excel(row=id, col=9, value='F')
            self.excel.create_excel(row=id,col=8,value=json.dumps(res,ensure_ascii=False))
            raise e
        else:
            my_log.info("用例--【编号为:{}，标题为:{}】---执行成功".format(items['case_id'], items['title']))
            self.excel.create_excel(row=id, col=9, value='T')
