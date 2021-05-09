"""
======================================
Author:包天宇
Time:2021-05-07 21:57
E-mail:uattb991492@icccuat.com
======================================
"""
import unittest
import os
import requests
import json
from jsonpath import jsonpath
from common.handle_path import DATA_DIR
from common.handle_excel import Excel
from unittestreport import ddt, list_data
from common.handle_conf import conf
from common.handle_mysql import HandleSql
from common.handle_log import my_log
from common.handle_com import res_asser_expected


@ddt
class TestRecharge(unittest.TestCase):
    # 充值功能
    excel = Excel(filename=os.path.join(DATA_DIR, 'case.xlsx'), sheetname='recharge')
    cases = excel.read_excel()
    mysql = HandleSql()
    base_url = conf.get('SIT','base_url')

    # 前置操作，登录一次登录系统，获取id
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
    def test_recharge(self, item):
        # url
        url = self.base_url + item['url']
        # 请求方法
        method = item['method'].lower()
        # 请求参数,并且将动态参数替换
        if "#member_id#" in item['data']:
            item['data'] = item['data'].replace("#member_id#",str(self.member_id))

        data = eval(item['data'])


        # 预期结果
        expected = eval(item['expected'])
        # excle写入的行数
        row_id = item['case_id'] +1
        # 请求之前，查询数据库，查看充值之前的金额
        sql = 'SELECT leave_amount FROM futureloan.member WHERE mobile_phone="{}"'.format(
            conf.get("login_data", 'mobile'))

        start_amount = self.mysql.find_one(sql)[0]
        my_log.info("请求之前的金额为：",start_amount)

        # 发送请求
        response = requests.request(method=method,url=url,json=data,headers=self.headers)
        res = response.json()

        # 请求之后，查询数据查看金额

        end_amount = self.mysql.find_one(sql)[0]
        my_log.info("请求之后的金额为：",end_amount)

        try:
            res_asser_expected(expected,res)
            # 对充值的金额进行断言
            # 充值成功，end-start = 充值金额data['amount']
            if item['check_sql']:
                self.assertEqual(float(end_amount-start_amount),float(data['amount']))
            # 充值失败，金额保存一致
            else:
                self.assertEqual(float(end_amount-start_amount),0)

        except AssertionError as e:
            my_log.error("用例--【模块为：{}，编号为:{}，标题为:{}】---执行失败".format(item['interface'], item['case_id'], item['title']))
            my_log.exception(e)
            self.excel.create_excel(row=row_id, col=9, value='F')
            self.excel.create_excel(row=row_id, col=8, value=json.dumps(res, ensure_ascii=False))
            raise e
        else:
            my_log.error("用例--【模块为：{}，编号为:{}，标题为:{}】---执行成功".format(item['interface'], item['case_id'], item['title']))
            self.excel.create_excel(row=row_id, col=9, value='T')



