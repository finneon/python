#!/usr/bin/env python
""" the __getattr__ magic method only gets invoked for attributes that are not in the __dict__ magic attribute """
import sys

class GetAttr:
    def __init__(self):
        self.__dict__['a'] = 'a'
        self.__dict__['b'] = 'b'

    def __getattr__(self, name):
        return 1234

if __name__ == '__main__':
    t = GetAttr()
    print "dict of t: %s" % t.__dict__.keys()
    print t.a
    print t.b
    print t.c
    t.c = 4321
    print "dict of t: %s" % t.__dict__.keys()
    print t.c
    t.a = 5432
    print t.a
