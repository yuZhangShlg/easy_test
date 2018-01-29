# -*-coding:utf-8
__author__ = 'yu.zhang4'

from flask import Flask, request, Response
import json

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'hello world'

@app.route('/json', methods=['POST'])
def my_json():
    print request.headers
    print request.json
    rt = {'info':'hello '+request.json['name']}
    return Response(json.dumps(rt),  mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)