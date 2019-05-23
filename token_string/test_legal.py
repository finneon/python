#!/usr/bin/env python

import re
import sys
import string

''' Check legal words 
    Legal word:
    1. Number only and accept leading '-' eg. -000000000001
    2. Letter only
    3. The legal words don't have punctuation eg:
      - -10- or 12A is not legal words
      - Neither_is_this
      - Not -1111- neither 1111-1111 1111_1111 1111/1111 !1000 ^1000 .1000
      - Note that dogs is legal word but not (except because it has )
'''


class Tokens:
    def __init__(self, file):
        self.file = file
        self.count_num = 0
        self.count_str = 0
        self.str_pattern = re.compile("^([A-Za-z]+$)")
        self.num_pattern = re.compile("^[0-9]+$")
        self.negative_num_pattern = re.compile("^-[0-9]+$")

    def handle_file(self):
        with open(self.file, 'r') as f:
            for line in f.readlines():
                self.handle_line(line)

    def handle_line(self, line):
        for word in line.split():
            if re.match(self.str_pattern, word):
                self.count_str += 1
            elif re.match(self.num_pattern, word) or re.match(self.negative_num_pattern, word):
                self.count_num += 1
            else:
                continue


def count_string(count_str, count_num):
    # Must use this func as request
    print("There are {0} strings and {1} numbers".format(count_str, count_num))


def main():
    if len(sys.argv[:1]) != 1:
        print("wrong argument")
        sys.exit(1)
    else:
        token = Tokens(sys.argv[1])
        token.handle_file()
        count_string(token.count_str, token.count_num)


if __name__ == "__main__":
    main()
