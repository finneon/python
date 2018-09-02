import unittest

import test_something
import test_something2
import test_something3

loader = unittest.TestLoader()

suite = loader.loadTestsFromModule(test_something)
suite.addTests(loader.loadTestsFromModule(test_something2))
suite.addTests(loader.loadTestsFromModule(test_something3))

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
