#!/usr/bin/env python

import re
import sys
import string

''' Check legal words 
    Legal word:
    - Number only and acceppt leading '-' eg. -000000000001
    - Letter only
    - The legal words don't have punctuation eg:
      + -10- is not legal words
      + Neither_is_this
      + Not -1111- neither 1111-1111 1111_1111 1111/1111 !1000 ^1000
      + Note that dogs is legal word but not (except because it has )
'''


class Tokens:
    def __init__(self, file):
        self.file = file
        self.count_num = 0
        self.count_str = 0

    def handle_file(self):
        with open(self.file, 'r') as f:
            for line in f.readlines():
                self.handle_line(line)

    def handle_line(self, line):
        for word in line.split():
            if re.search('[0-9]', word) and re.search('[A-Za-z]', word):
                continue
            elif re.search('[0-9]', word):
                if re.search('-', word) and word.startswith('-'):
                    # Remove the first '-' to check if number -10- or --10
                    if re.sub('-', '', word, 1).isdigit():
                        self.count_num += 1
                    else:
                        continue
                elif self.check_punctuation(word):
                    continue
                else:
                    self.count_num += 1
            elif re.search('[A-Za-z]', word):
                if not self.check_punctuation(word):
                    self.count_str += 1

    @staticmethod
    def check_punctuation(word):
        # Return True if there's punctuation
        if len(['' for i in list(word) if i in string.punctuation]) == 0:
            return False
        return True


def count_string(count_str, count_num):
    # Must use this func as request
    print("There are {0} strings and {1} numbers".format(count_str, count_num))


def main():
    if len(sys.argv[:1]) > 1:
        print("wrong argument")
        sys.exit(1)
    else:
        token = Tokens(sys.argv[1])
        token.handle_file()
        count_string(token.count_str, token.count_num)


if __name__ == "__main__":
    main()
