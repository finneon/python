#!/usr/bin/env python
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

    def display(self):
        r = requests.get(self.url, headers={'app_id': self.app_id, 'app_key': self.app_key})
        data = json.loads(json.dumps(r.json()))
        str = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
        str_split = str.split()
        chunck, chunck_size = len(str_split), len(str_split)/3
        print (bcolors.BOLD + bcolors.YELLOW + self.word + bcolors.ENDC)
        print "\n".join([" ".join(str_split[i:i+chunck_size]) for i in range(0, chunck, chunck_size)])


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
