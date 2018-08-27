#!/bin/usr/env python

import os
import subprocess as sub
import unittest
import json


class TestDeletePetStore(unittest.TestCase):
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

    def test_deletePetStore(self):
        print "Test delete pet\n"

        print "First check if the pet exists\n"
        self.assertTrue(self.check_pet(), "Check pre-condition")

        print "Delete pet\n"
        sub.check_output([self.cmd, "delete", self.pet_id])
        self.assertFalse(self.check_pet(), "Failed to delete pet {}".format(self.pet_id))
        print "Test done\n"

if __name__ == '__main__':
    unittest.main()