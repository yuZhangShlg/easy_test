# -*-coding:utf-8
__author__ = 'yu.zhang4'

# from flask import Flask,url_for
#
# app = Flask(__name__)

# @app.route('/login')
# def index():
#    pass

# with app.test_request_context():
#    print url_for('index',a='1')

####### 蓝图
from flask import Blueprint,render_template,abort,url_for
from jinja2 import TemplateNotFound

simple_page = Blueprint('simple_page',__name__,template_folder='templates')

@simple_page.route('/',defaults={'page':'index'})
@simple_page.route('/<page>')

def show(page):
    try:
        return render_template('pages/%s.html' %page)
    except TemplateNotFound:
        abort(404)

# print simple_page.root_path

admin = Blueprint('admin', __name__, static_folder='static')








