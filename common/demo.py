"""
======================================
Author:包天宇
Time:2021-04-28 22:39
E-mail:uattb991492@icccuat.com
======================================
"""
from common.handle_com import str_dict
import requests
from common.handle_conf import conf
from jsonpath import jsonpath

s_json = '{"aa": null, "bb": "python", "cc": true, "dd": false, "ee": [11, 22, 33]}'


# 将json字符文件转为对应的pytho串转换为对应的python数据
# res = json.loads(s_json)
# print(res)

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
print(res)
id = jsonpath(res,'$..id')
token = jsonpath(res,'$..token')
print(id)
print(token)