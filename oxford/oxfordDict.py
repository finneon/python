#!/usr/bin/env python
'''
    Search Dictionaries
    www.oxfordlearnersdictionaries.com/ or https://en.oxforddictionaries.com/
    REST API documentation: https://www.oxfordlearnersdictionaries.com/api/v1/documentation/html
    Register for app_key: https://developer.oxforddictionaries.com/
'''
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

class OxfordDict():
    def __init__(self, word):
        self.word = word
        self.app_id = "79b0bf7f"
        self.app_key = "e1c41553a15e7ab359b36ec3a849e2b4"
        self.language = 'en'
        self.url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + self.language + '/' \
                          + self.word.lower()
        self.count_def = 1
        self.word_type_dict = {"Noun": "n", "Verb": "v", "Adjective": "adj", "Adverb": "adv"}

    def build_data(self):
        """
        Build data: {word type: [senses, pron]}
        - Each item of 'lexicalEntries' is a word type that is defined in 'lexicalCategory'
          and it contains definitions and examples
        """
        r = requests.get(self.url, headers={'app_id': self.app_id, 'app_key': self.app_key})
        if r.status_code == 404:
            print(bcolors.BOLD + "\"" + self.word + "\"" + bcolors.ENDC + " Not Found")
            sys.exit(0)
        json_dump = json.loads(json.dumps(r.json()))
        data = {}
        for lex_dict in json_dump['results'][0]['lexicalEntries']:
            word_type = lex_dict['lexicalCategory']
            senses = lex_dict['entries'][0]['senses'][0]
            pron = lex_dict['pronunciations'][0]['phoneticSpelling']
            data[word_type] = [senses, pron]
        return data

    def display(self, type_get):
        """
        Display the main definition of word and examples.
        Then display the subsenses and examples
        """

        def chunk_str(str_def):
            """ Split the string by 2 for nice print """
            if len(str_def) > 80:
                str_split = str_def.split()
                chunk, chunk_size = len(str_split), len(str_split) / 2
                str_def = "\n".join([" ".join(str_split[i:i + chunk_size]) for i in range(0, chunk, int(chunk_size))])
            return str_def

        def display_examples(examples):
            for e in examples:
                print(bcolors.BOLD + bcolors.RED + "%3s %s" % (".", e['text']) + bcolors.ENDC)
            print("\r")

        def display_subsenses(subsenses, order):
            """ Loop all the subsenses and their examples """
            count = 1
            sub_note_text = ""
            for subsense in subsenses:
                if 'notes' in subsense:
                    tmp_note = subsense['notes'][0]['text']
                    if tmp_note.find('"') != -1:
                        tmp_note = re.sub('"', "", tmp_note)
                        sub_note_text = "({})".format(tmp_note)
                    else:
                        sub_note_text = "[{}]".format(tmp_note)
                _def = subsense['definitions'][0]
                item = "{}.{} {}".format(order, count, sub_note_text)
                print("%5s %s" % (item, _def))
                count += 1
                if 'examples' in subsense:
                    display_examples(subsense['examples'])

        data = self.build_data()
        for word_type, content in data.items():
            if type_get:
                if self.word_type_dict[word_type] != type_get:
                    continue

            note_text = ""
            pron = content[1]
            sense = content[0]
            if 'notes' in sense:
                note_text = "[{}]".format(sense['notes'][0]['text'])

            print(bcolors.BOLD + bcolors.YELLOW + "%s /%s/ (%s)" % (self.word, pron, self.word_type_dict[word_type]) \
                  + bcolors.ENDC)
            print("{0}. {1} {2}".format(str(self.count_def), note_text, chunk_str(sense['definitions'][0])))

            if 'examples' in sense:
                display_examples(sense['examples'])

            if 'subsenses' in sense:
                display_subsenses(sense['subsenses'], self.count_def)

            self.count_def += 1


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
