#!/bin/usr/env python

import os
import subprocess as sub
import unittest
import json


class TestModifyPetStore(unittest.TestCase):
    def setUp(self):
        self.cmd = os.path.realpath(os.path.join(os.getcwd(), "petStore.py"))
        self.pet_name = "pussy_cat"
        self.pet_id = "2018"

    def check_pet(self):
        output = sub.check_output([self.cmd, "get", self.pet_id])
        if str(output).strip() == "Pet not found":
            return False
        else:
            return True

    def test_modifyPetStore(self):
        print "Test modify pet\n"

        print "Check pet\n"
        self.assertTrue(self.check_pet(), "pet does not exsit, check pre-condition")

        print "Modify pet name\n"
        output = sub.check_output([self.cmd, "post", "pussy_dog", self.pet_id])
        js_output = json.loads(output)
        self.assertEqual(self.pet_id, str(js_output['id']))
        self.assertEqual("pussy_dog", js_output['name'])
        print "Test done\n"

if __name__ == '__main__':
    unittest.main()