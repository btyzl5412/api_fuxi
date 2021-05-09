"""
======================================
Author:包天宇
Time:2021-05-09 20:47
E-mail:uattb991492@icccuat.com
======================================
"""
import unittest
import os
import requests
import json
from jsonpath import jsonpath
from unittestreport import ddt, list_data
from common.handle_path import DATA_DIR
from common.handle_excel import Excel
from common.handle_mysql import HandleSql
from common.handle_conf import conf
from common.handle_log import my_log
from common.handle_com import res_asser_expected


@ddt
class TestWithward(unittest.TestCase):
    excel = Excel(filename=os.path.join(DATA_DIR, 'case.xlsx'), sheetname='withdraw')
    cases = excel.read_excel()
    mysql = HandleSql()
    base_url = conf.get('SIT', 'base_url')

    # 前置条件，登录获取id和token
    @classmethod
    def setUpClass(cls) -> None:
        # url地址
        url = conf.get('SIT', 'base_url') + '/member/login'

        # 请求参数
        data = {
            "mobile_phone": conf.get('login_data', 'mobile'),
            "pwd": conf.get('login_data', 'pwd')
        }

        # 请求头
        headers = eval(conf.get('SIT', 'headers'))

        # 发送请求
        response = requests.post(url=url, json=data, headers=headers)
        res = response.json()

        # 获取token,并且将token写入请求头headers中
        token = jsonpath(res, '$..token')[0]
        headers["Authorization"] = "Bearer " + token

        # 获取id
        id = jsonpath(res, '$..id')[0]

        # 将headers和id设置为类属性
        cls.headers = headers
        cls.member_id = id

    @list_data(cases)
    def test_withward(self, item):
        # url
        url = self.base_url + item['url']
        # 请求方法
        method = item['method']
        # 预期结果
        expected = eval(item['expected'])
        # row_id
        row_id = item['case_id'] + 1

        # 请求之前的用户余额
        sql = 'SELECT leave_amount FROM futureloan.member WHERE id="{}"'.format(
            self.member_id)

        # 请求参数
        if "#member_id#" in item['data']:
            item['data'] = item['data'].replace('#member_id#', str(self.member_id))

        if "#amount#" in item['data']:
            amount = self.mysql.find_one(sql=sql)[0] + 10000
            item['data'] = item['data'].replace('#amount#', str(amount))
            print(item['data'])

        data = eval(item['data'])

        # 请求之前的余额
        start_amount = self.mysql.find_one(sql=sql)[0]
        my_log.info('请求之前的余额{}'.format(start_amount))

        # 发送请求
        response = requests.request(method=method, url=url, json=data, headers=self.headers)
        res = response.json()

        # 请求完成后的余额
        end_amount = self.mysql.find_one(sql=sql)[0]
        my_log.info('请求之前的余额{}'.format(end_amount))

        # 进行断言
        try:
            res_asser_expected(expected, res)
            # 数据库余额的断言，提现成功，余额减少，提现失败，余额不变
            if item['check_sql'] == 1:
                self.assertEqual(float(start_amount - end_amount), float(data['amount']))
            else:
                self.assertEqual(float(start_amount - end_amount), 0)
        except AssertionError as e:
            my_log.error("用例--【模块为：{}，编号为:{}，标题为:{}】---执行失败".format(item['interface'], item['case_id'], item['title']))
            my_log.exception(e)
            self.excel.create_excel(row=row_id, col=9, value='F')
            self.excel.create_excel(row=row_id, col=8, value=json.dumps(res, ensure_ascii=False))
            raise e
        else:
            my_log.error("用例--【模块为：{}，编号为:{}，标题为:{}】---执行成功".format(item['interface'], item['case_id'], item['title']))
            self.excel.create_excel(row=row_id, col=9, value='T')
