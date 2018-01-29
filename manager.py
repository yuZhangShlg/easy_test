# -*-coding:utf-8
__author__ = 'yu.zhang4'

from flask import Flask
from views.cmdb_query import cmdb_query


app = Flask(__name__)

# app.register_module(cmdb_query, url_prefix='/cmdbQuery')
app.register_blueprint(cmdb_query)


if __name__ == '__main__':    # 确保服务器只会在该脚本被python解释器执行的时候才会运行
#    app.run()                 # run()函数让应用运行在本地服务器
     app.debug = True
     app.run()