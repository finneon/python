#!/usr/bin/env python
import sys

class TestItems:
    def __init__(self):
        pass

    def __getitem__(self, items):
        print ("%-15s %s" % (type(items), items))

if __name__ == '__main__':
    c = TestItems()
    c[sys.argv[1]]
