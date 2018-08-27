#!/bin/usr/env python

import os
import subprocess as sub
import unittest
import json


class TestCreatePetStore(unittest.TestCase):
    def setUp(self):
        self.cmd = os.path.realpath(os.path.join(os.getcwd(), "petStore.py"))
        self.pet_name = "pussy_cat"
        self.pet_id = "2018"

    def test_createPetStore(self):
        print "Test create pet store\n"
        print "Create pet"
        output = sub.check_output([self.cmd, "add", self.pet_name, self.pet_id])
        js_output = json.loads(output)
        self.assertEqual(self.pet_id, str(js_output['id']))
        self.assertEqual(self.pet_name, js_output['name'])
        print "Test done\n"

if __name__ == '__main__':
    unittest.main()