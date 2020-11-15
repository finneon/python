#!/bin/python3
import math
import os
import random
import re
import sys


#
# Complete the 'maximumOccurringCharacter' function below.
#
# The function is expected to return a CHARACTER.
# The function accepts STRING text as parameter.
#

def maximumOccurringCharacter(text):
    # Write your code here
    #str_text = text.lower()
    str_text = text
    char_dict = dict()

    """ Define dict of all chars """
    for i in str_text:
        if i not in char_dict:
            char_dict[i] = 0
        
    """ Count the chars in string """
    for char in str_text:
        for key in char_dict.keys():
            if key == char:
                char_dict[key] += 1
    
    """ Find the first maximum char """
    max_num = 0
    max_char = ''
    for key, value in char_dict.items():
        if value > max_num:
            max_num = value
            max_char = key
    return max_char


if __name__ == '__main__':
     maximumOccurringCharacter(sys.argv[1])
