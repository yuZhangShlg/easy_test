# -*-coding:utf-8
__author__ = 'yu.zhang4'

class Test():
    def __enter__(self):
        print "In __enter__()"
        return "test_with"
    def __exit__(self, type, value, trace):
        print "In __exit__()"

def get_example():
    return Test()

with get_example() as example:
    print "example:", example