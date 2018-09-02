"""
    Test order:
        - testCreatePet
        - testModifyPet
        - testDeletePet
"""
import unittest

import os, sys
import fnmatch
import importlib

test_file = fnmatch.filter(os.listdir("."), "test*.py")
test_file.sort()
mod_list = []
for tfile in test_file:
    mod = importlib.import_module(os.path.splitext(tfile)[0])
    mod_list.append(mod)

# Initialize test suite
suite = unittest.TestSuite()
loader = unittest.TestLoader()

# Add tests to the test suite in order: create, modify and delete
suite.addTest(loader.loadTestsFromModule(mod_list[0]))
suite.addTest(loader.loadTestsFromModule(mod_list[-1]))
suite.addTest(loader.loadTestsFromModule(mod_list[1]))

# Initialize test runner, pass it our suite and run them
print "Run test\n"
runner = unittest.TextTestRunner(verbosity=3)
runner.run(suite)
