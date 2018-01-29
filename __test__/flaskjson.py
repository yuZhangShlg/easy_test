# -*-coding:utf-8
__author__ = 'yu.zhang4'

from flask import Flask
from flask import json
from flask import Response

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello(name, words):
    return json.dumps({'name': name, 'words': words})

if __name__ == '__main__':
    app.run()