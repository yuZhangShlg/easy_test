# -*-coding:utf-8
__author__ = 'yu.zhang4'

from flask import Flask
from __test__.admin import admin
from user import user

app = Flask(__name__)
#这里分别给app注册了两个蓝图admin,user
#参数url_prefix='/xxx'的意思是设置request.url中的url前缀，
#即当request.url是以/admin或者/user的情况下才会通过注册的蓝图的视图方法处理请求并返回
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')