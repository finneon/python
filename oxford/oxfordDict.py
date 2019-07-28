#!/usr/bin/env python
"""
    Search Dictionaries
    www.oxfordlearnersdictionaries.com/ or https://en.oxforddictionaries.com/
    REST API documentation: https://www.oxfordlearnersdictionaries.com/api/v1/documentation/html
    Register for app_key: https://developer.oxforddictionaries.com/
"""
import requests
import json
import argparse
import sys
import re

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\33[3m'
    SELECTED = '\33[7m'

class OxfordDict(object):
    def __init__(self, word):
        self.word = word
        self.app_id = "79b0bf7f"
        self.app_key = "f881171db1e3e7a750bd2bf250683428"
        self.language = 'en-us'
        self.url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + self.language + '/' + self.word.lower()
        self.word_type_dict = {"Noun": "n", "Verb": "v", "Adjective": "adj", "Adverb": "adv"}

    def build_data(self):
        """
        Build data: List of {word_type: [senses, pron]}
        - Each item of 'lexicalEntries' is a word type that is defined in 'lexicalCategory'
          and it contains definitions and examples
        - senses: array of dicts which contain definition + subsenses
        """
        r = requests.get(self.url, headers={'app_id': self.app_id, 'app_key': self.app_key})
        if r.status_code == 404:
            print(bcolors.BOLD + bcolors.YELLOW + "\"" + self.word + "\"" + bcolors.ENDC + " Not Found")
            sys.exit(0)
        json_dump = json.loads(json.dumps(r.json()))
        data = {}
        for lex_dict in json_dump['results'][0]['lexicalEntries']:
            word_type = lex_dict['lexicalCategory']['text']
            senses = lex_dict['entries'][0]['senses']
            pron = lex_dict['pronunciations'][0]['phoneticSpelling']
            data[word_type] = [senses, pron]
        return data

    @staticmethod
    def chunk_str(str_def):
        """ Split the string by 2 for nice print """
        if len(str_def) > 15:
            str_split = str_def.split()
            str_def = "\n".join([" ".join(str_split[i:i + 15]) for i in range(0, len(str_split), 15)])
        return str_def

    @staticmethod
    def display_examples(examples):
        for e in examples:
            print(bcolors.BOLD + bcolors.RED + "%3s %s" % (".", e['text']) + bcolors.ENDC)

    @staticmethod
    def display_subsenses(subsense_dict, order):
        """ Loop all the subsenses and their examples """
        count = 1
        for subsense in subsense_dict:
            type_sub_def = OxfordDict.get_type_of_def(subsense)
            if type_sub_def:
                type_sub_def = " " + type_sub_def + " "
            _def = subsense['definitions'][0]
            print(" %s.%s" % (order, count) +
                  bcolors.ITALIC + bcolors.GREEN + "%1s" % type_sub_def + bcolors.ENDC +
                  "%s" % OxfordDict.chunk_str(_def))
            count += 1
            if 'examples' in subsense:
                OxfordDict.display_examples(subsense['examples'])
            print("\r")

    @staticmethod
    def get_type_of_def(sense_dict):
        regions = None
        registers = None
        notes = None
        if 'notes' in sense_dict:
            tmp_note = sense_dict['notes'][0]['text']
            if tmp_note.find('"') != -1:
                tmp_note = re.sub('"', "", tmp_note)
                notes = "({})".format(tmp_note)
            else:
                notes = "[{}]".format(tmp_note)
        if 'regions' in sense_dict:
            regions = sense_dict['regions'][0]
        if 'registers' in sense_dict:
            registers = sense_dict['registers'][0]

        return " ".join(filter(lambda x: x is not None, [regions, registers, notes]))

    def display(self, type_get):
        """
        Display the main definition of word and examples.
        Then display the subsenses and examples
        """
        data = self.build_data()
        for word_type, content in data.items():
            count_def = 1
            if type_get and self.word_type_dict[word_type] != type_get:
                continue
            pron = content[1]
            print(bcolors.BOLD + bcolors.YELLOW + "%s /%s/ (%s)" % (self.word, pron, self.word_type_dict[word_type])
                  + bcolors.ENDC)
            for sense_dict in content[0]:
                type_def = self.get_type_of_def(sense_dict)
                if type_def:
                    type_def = " " + type_def + " "
                print("%s." % str(count_def) +
                      bcolors.ITALIC + bcolors.GREEN + "%1s" % type_def + bcolors.ENDC +
                      "%s" % self.chunk_str(sense_dict['definitions'][0]))
                if 'examples' in sense_dict:
                    self.display_examples(sense_dict['examples'])

                print("\r")

                if 'subsenses' in sense_dict:
                    self.display_subsenses(sense_dict['subsenses'], count_def)

                print("\r")
                count_def += 1


def parse_argument(args):
    parser = argparse.ArgumentParser(description="Oxford learner's dictionaries",
                                     epilog="Search OALD")
    parser.add_argument("input", type=str, nargs=1,
                        help="Input word to search")
    parser.add_argument("-t", "--type", type=str, nargs=1, dest="word_type",
                        help="Type of word: n|v|adj|adv")

    options = parser.parse_args(args=args)
    return options


def main():
    options = parse_argument(sys.argv[1:])
    oxf = OxfordDict(options.input[0])

    word_type = ""
    if options.word_type:
        word_type = options.word_type[0]
        if word_type not in oxf.word_type_dict.values():
            print("No Type of word\n\nType of word: n|v|adj|adv")
            sys.exit(1)
    oxf.display(word_type)


if __name__ == "__main__":
    main()
