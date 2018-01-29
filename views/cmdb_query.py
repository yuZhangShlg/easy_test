# -*-coding:utf-8
__author__ = 'yu.zhang4'

from flask import Flask,request,Response,Blueprint,jsonify,render_template   # 导入Flask模块
import requests,json
from decorator import ArgumentRequired
from flask_sso import login_required

cmdb_query = Blueprint('cmdb_query',__name__)

#####  s实用GET获取参数
# @cmdb_query.route('/',methods=['GET'])         # route()装饰器告诉Flask什么样的URL能触发函数
# def hello_word():   # 生成URL是被采用，显示信息
#     a = request.values.get('a')
#     if a==None:
#         return render_template('test.html',a=a)
#     else:
#         b = int(a) + 1
#     return render_template('test.html',b=list(range(1,10)),a=a)

# @cmdb_query.route('/json',methods=['POST'])         # route()装饰器告诉Flask什么样的URL能触发函数
# def hello_word_post():   # 生成URL是被采用，显示信息
#     a = request.get_data()
#     a = json.loads(a)
#     for i in a:
#         a[i] = i*10
#     return Response(json.dumps(a), mimetype='application/json')

# @cmdb_query.route('/',methods=['POST'])         # route()装饰器告诉Flask什么样的URL能触发函数
# def hello_word():   # 生成URL是被采用，显示信息
#     data =json.loads(request.data)
#     if data.get("selRollBack") == "selRollBack":
#         return jsonify({"success":True})
#     else:
#         return jsonify({"success":False})


@cmdb_query.route('/',methods=['GET'])         # route()装饰器告诉Flask什么样的URL能触发函数
# @login_required
def test_with():   # 生成URL是被采用，显示信息
     with ArgumentRequired('taskid'):
        return 'hello word'