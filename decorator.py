#_*_coding:utf-8
__author__ = 'Dell'

from flask import request, current_app
from exception import InvalidUsageError
import json


class ArgumentRequired(object):
    def __init__(self, *args):
        self.args = args

    def __enter__(self):
        for arg in self.args:
            if arg in ('taskId','taskid','taskId1'):
                raise InvalidUsageError('argument {0} is required'.format(arg), status_code=400)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass