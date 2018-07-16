#!/usr/bin/env python

import sys
from cStringIO import StringIO
import logging
import unittest
import os

class TestException(Exception):
    def __init__(self, value):
        self.__value = value
        Exception.__init__(self, 'Exception message: %s' % value)

    def __str__(self):
        return repr(self.__value)

class NoErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR

class StringRedirect:
    def __init__(self):
        os.system("rm -f log.txt")
        self.old_stderr = None
        self.old_stdout = None
        self.output = StringIO()
        self.txt = ""

    def start_capture_output(self):
        self.old_stderr = sys.stderr
        self.old_stdout = sys.stdout
        self.txt = ""
        self.output.seek(0)
        sys.stderr = sys.stdout = self.output

    def stop_capture_output(self):
        self.output.seek(0)
        self.txt = "".join(self.output.readlines())
        self.output.seek(0)
        self.output.reset()
        sys.stderr = self.old_stderr
        sys.stdout = self.old_stdout
        print "\n#", self.txt

    def test_error(self):
        logging.error("error message") # Send log record to console
        raise TestException("tcg exception message")

    def init_logger(self, name):
        self.noerr = NoErrorFilter()

        if name is not None:
            self.logger = logging.getLogger(name)
        else:
            self.logger = logging.getLogger()
            self.logger.setLevel(logging.DEBUG)

        self.handler = logging.FileHandler("log.txt")
        self.handler.setLevel(logging.DEBUG)
        self.handler.setFormatter((logging.Formatter(
            "[%(name)s][%(filename)s:%(lineno)d]: %(levelname)s - FILE %(message)s")))
        self.logger.addHandler(self.handler)

        self.stdout = logging.StreamHandler(sys.stdout)
        self.stdout.setLevel(logging.DEBUG)
        self.stdout.setFormatter((logging.Formatter(
            "[%(name)s][%(filename)s:%(lineno)d]: %(levelname)s - OUT %(message)s")))
        self.stdout.addFilter(self.noerr)
        self.logger.addHandler(self.stdout)

        self.stderr = logging.StreamHandler(sys.stderr)
        self.stderr.setLevel(logging.DEBUG)
        self.stderr.setFormatter((logging.Formatter(
            "[%(name)s][%(filename)s:%(lineno)d]: %(levelname)s - ERR %(message)s")))
        self.logger.addHandler(self.stderr)

    def remove_handlers(self):
        self.logger.handlers = []

class TestStringMethods(unittest.TestCase):
    def test_except_1_root(self):
        tmpstderr = sys.stderr
        sys.stderr = StringIO() # redirect all stderr to this object file

        sr.init_logger("")
        sr.start_capture_output()
        with self.assertRaises(TestException) as err:
            sr.test_error()

        sr.stop_capture_output()
        content = sys.stderr.getvalue()

        self.assertRegexpMatches(content, 'error message')
        self.assertRegexpMatches(str(err.exception), 'tcg exception message')
        sys.stderr = tmpstderr
        sr.remove_handlers()

    def test_except_2_name(self):
        tmpstderr = sys.stderr
        sys.stderr = StringIO() # redirect all stderr to this object file

        sr.init_logger("test")
        sr.start_capture_output()
        with self.assertRaises(TestException) as err:
            sr.test_error()

        sr.stop_capture_output()
        content = sys.stderr.getvalue()

        self.assertRegexpMatches(content, 'error message')
        self.assertRegexpMatches(str(err.exception), 'tcg exception message')
        sys.stderr = tmpstderr
        sr.remove_handlers()

sr = StringRedirect()
suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
unittest.TextTestRunner(verbosity=2).run(suite)
