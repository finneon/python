# Enter your code here. 
# Complete the classes below.
# Reading the inputs and writing the outputs are already done for you.
#
class LetterFilter:

    def __init__(self, s):
        self.s = s
        self.vowel_list = ['a', 'e', 'i', 'o', 'u']
        
	
    def filter_vowels(self):
        remain_str = list()
        for char in self.s:
            if char not in self.vowel_list:
                remain_str.append(char)
        return ''.join(remain_str)
        
        
    def filter_consonants(self):
        remain_str = list()
        for char in self.s:
            if char in self.vowel_list:
                remain_str.append(char)
        return ''.join(remain_str)


s = input()
