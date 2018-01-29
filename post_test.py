# -*-coding:utf-8
__author__ = 'yu.zhang4'

import requests,json

user_info = list(range(10))
headers = {'content-type': 'application/json'}
r = requests.post("http://127.0.0.1:5000/json", data=json.dumps(user_info), headers=headers)

print r.text

