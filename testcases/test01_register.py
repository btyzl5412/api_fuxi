"""
======================================
Author:包天宇
Time:2021-04-28 21:35
E-mail:uattb991492@icccuat.com
======================================
"""
import unittest
import os
import requests
import json
from common.handle_excel import Excel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from unittestreport import ddt, list_data
from common.handle_com import *
from common.handle_log import my_log
from common.handle_mysql import HandleSql


@ddt
class TestRegister(unittest.TestCase):
    # 读取测试用例(注册功能)
    excle = Excel(os.path.join(DATA_DIR, 'case.xlsx'), 'register')
    cases = excle.read_excel()
    # 连接数据库
    my_sql = HandleSql()
    # 请求头
    headers = eval(conf.get('SIT', 'headers'))
    # 基础url
    base_url = conf.get('SIT', 'base_url')

    @list_data(cases)
    def test_register(self, items):
        # 测试数据的准备
        # 1.接口地址
        url = self.base_url + items['url']
        # 2.请求方法(小写)
        method = items['method'].lower()
        # 3.请求参数,将手机号进行替换
        if "#phone#" in items['data']:
            phone = random_phone()
            items['data'] = items['data'].replace("#phone#", phone)
        # data = eval(items['data'])
        data = json.loads(items['data'])
        # 4.预期结果
        expected = eval(items['expected'])
        # 5.行数
        rows = items['case_id'] + 1

        # 请求接口
        response = requests.request(method=method, url=url, json=data, headers=self.headers)
        res = response.json()
        # 打印请求结果
        # print('请求结果', res)
        # 进行断言
        try:
            res_asser_expected(expected, res)
            # 对数据库中的数据进行检验
            if items['check_sql']:
                sql = items['check_sql'].format(phone)
                count = self.my_sql.find_count(sql)
                my_log.info("查询数据库的结果为:{}".format(count))
                self.assertEqual(count, 1)

        except AssertionError as e:
            my_log.error("用例--【编号为:{}，标题为:{}】---执行失败".format(items['case_id'], items['title']))
            my_log.exception(e)
            # 将数据返显至excel
            self.excle.create_excel(row=rows, col=9, value='F')
            self.excle.create_excel(row=rows, col=8, value=json.dumps(res, ensure_ascii=False))
            raise e
        else:
            my_log.info("用例--【编号为:{}，标题为:{}】---执行成功".format(items['case_id'], items['title']))
            self.excle.create_excel(row=rows, col=9, value='T')

