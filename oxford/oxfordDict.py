#!/usr/bin/env python
'''
    Search Dictionaries
    www.oxfordlearnersdictionaries.com/
    REST API documentation: https://www.oxfordlearnersdictionaries.com/api/v1/documentation/html
    Register for app_key: https://developer.oxforddictionaries.com/
'''
import requests
import json
import argparse
import sys

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class OxfordDict():
    def __init__(self, word):
        self.word = word
        self.app_id = "79b0bf7f"
        self.app_key = "e1c41553a15e7ab359b36ec3a849e2b4"
        self.language = 'en'
        self.url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + self.language + '/' \
                          + self.word.lower()
        self.count_def = 1

    def chunk_str(self, str_def):
        ''' Split the string by 2 for nice print '''
        if len(str_def) > 80:
            str_split = str_def.split()
            chunk, chunk_size = len(str_split), len(str_split) / 2
            str_def = "\n".join([" ".join(str_split[i:i+chunk_size]) for i in range(0, chunk, chunk_size)])
        return str_def

    def display(self):
        '''
        Display the main definition of word and examples.
        Then display the subsenses and examples
        '''
        r = requests.get(self.url, headers={'app_id': self.app_id, 'app_key': self.app_key})
        data = json.loads(json.dumps(r.json()))
        definition = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
        examples = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['examples']
        print ("  " + bcolors.BOLD + bcolors.YELLOW + self.word + bcolors.ENDC)
        print (str(self.count_def) + ". " + self.chunk_str(definition))
        self.count_def += 1
        for i in range(0, len(examples), 1):
            print (bcolors.BOLD + bcolors.RED + "  . " + bcolors.ENDC + examples[i]['text'])

        subsenses = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['subsenses']
        self.display_subsenses(subsenses)

    def display_subsenses(self, str_sub):
        '''
        Loop all the subsenses and their examples
        '''
        for i in range(0, len(str_sub), 1):
            _def = str_sub[i]['definitions'][0]
            print str(self.count_def) + ". " + _def
            self.count_def += 1
            if 'examples' in str_sub[i]:
                _example = str_sub[i]['examples']
                for i in range(0, len(_example), 1):
                    print (bcolors.BOLD + bcolors.RED + "  . " + bcolors.ENDC + _example[i]['text'])

def parse_argument(args):
    parser = argparse.ArgumentParser(description="Oxford learner's dictionaries",
                                     epilog="Search OALD")
    parser.add_argument("input", type=str, nargs=1,
                        help="Input word to search")

    parser.parse_args(args=args)

def main(args):
    parse_argument(args)
    oxf = OxfordDict(args[0])
    oxf.display()

if __name__ == "__main__":
    main(sys.argv[1:])  