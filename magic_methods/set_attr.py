#!/usr/bin/env python
""" all attribute assignments go through __setattr__ """
import sys
import pdb; pdb.set_trace()

class Test(object):
    def __init__(self):
        self.a = 'a'
        self.b = 'b'

    def __setattr__(self, name, value):
        print 'set %s to %s' % (name, repr(value))

        if name in ('a', 'b'):
            object.__setattr__(self, name, value)

if __name__ == '__main__':
    t = Test()
    t.c = 'z'
