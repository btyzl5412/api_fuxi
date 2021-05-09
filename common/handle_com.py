"""
======================================
Author:包天宇
Time:2021-04-28 21:46
E-mail:uattb991492@icccuat.com
======================================
"""
import random
import string
import json


def random_phone():
    """
    随机生成手机号
    :return: 返回手机号
    """
    num_start = [
        '134', '135', '136', '137', '138',
        '139', '150', '151', '152', '158',
        '159', '157', '182', '187', '188',
        '147', '130', '131', '132', '155',
        '156', '185', '186', '133', '153',
        '180', '189']

    # 随机获取一个手机号码头部
    start = random.choice(num_start)
    # 随机生成8位数
    # string.digits 结果为0-9
    end = ''.join(random.sample(string.digits, 8))
    phone = start + end
    return phone


def res_asser_expected(expected, res):
    """
    自定义判断实际结果和预期结果
    :param res: 实际结果
    :param expected: 预期结果
    :return:
    """
    for k, v in expected.items():
        if res[k] == v:
            pass
        else:
            raise AssertionError("{} not in {}".format(expected, res))


def str_dict(s: str):
    """
    将字符串转换为字典
    :param s: 字符串
    :return:
    """
    try:
        res = eval(s)
    except:
        res = json.loads(s)

    return res
