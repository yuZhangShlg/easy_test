# -*-coding:utf-8
__author__ = 'yu.zhang4'

# import sys
# class test:
#     def __enter__(self):
#        print("enter")
#        return 1
#     def __exit__(self,*args):
#        print("exit")
#        return True
# with test() as t:
#     print("t is not the result of test(), it is __enter__ returned")
#     print("t is 1, yes, it is {0}".format(t))
#     raise NameError("Hi there")
#     sys.exit()
#     print("Never here")

# class Test():
#     def __enter__(self):
#         print "In __enter__()"
#         return "test_with"
#     def __exit__(self, type, value, trace):
#         print "In __exit__()"
#
# def get_example():
#     return Test()
#
# with get_example() as example:
#     print "example:", example

# import json
# from flask import request,jsonify
# from exception import InvalidUsageError
#
# class ArgumentJsonRequired(object):
#     def __init__(self, *args):
#         self.args = args
#
#     def __enter__(self):
#         data = json.loads(request.data)
#         for arg in self.args:
#             if arg not in data:
#                 raise InvalidUsageError(
#                     "argument {0} is required".format(arg), status_code=400)
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         pass
#
#
# with ArgumentJsonRequired('product_name'):
#     pass
from flask import json, request











