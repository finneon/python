#!/usr/bin/env python

from pyosaf.utils.immom.ccb import Ccb
from pyosaf.utils.immom.object import ImmObject

""" Test create IMM Objects using pyOsaf API """

class CreateObject:
    def __init__(self, class_name, attributes, dn):
        self.class_name = class_name
        self.attributes = attributes
        self.dn = dn
        if len(self.dn.split(',')) > 1:
            self.parent = self.dn.split(',')[1]
        else:
            self.parent = None
        self.obj = None

    def init_obj(self):
        self.obj = ImmObject(class_name=self.class_name, dn=self.dn)
        import pdb;pdb.set_trace()
        for attr in self.attributes.keys():
            self.obj.attrs[attr] = (self.obj.get_value_type(attr), [self.attributes[attr]]) 

    def init_ccb(self):
        ccb = Ccb(flags=None)
        ccb.init()

        ccb.create(self.obj, parent_name=self.parent)
        ccb.apply()
        ccb.finalize()
    
    def main(self):
        self.init_obj()
        self.init_ccb()

if __name__ == "__main__":
    c_attr_dict = {'attribute1': 'a1', 'attribute2': 'a2', 'sampleClassId': 'sampleClassId=1'}
    c_dn = 'sampleClassId=1'
    c = CreateObject("SampleClass1", c_attr_dict, c_dn)
    c.main()

    d_attr_dict = {'lowerCaps': 'low', 'upperCaps': 'up', 'capsId': 'capsId=1'}
    d_dn = 'capsId=1,sampleClassId=1'
    d = CreateObject("CapsSample", d_attr_dict, d_dn)
    d.main()