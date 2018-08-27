#!/usr/bin/env python

import argparse
import sys
import json
import os
import subprocess as sub

class Pet():
    def __init__(self):
        self.main_action = ""
        self.pet_name = ""
        self.pet_id = ""
        self.url = ""
        self.pre_url = "https://petstore.swagger.io/v2/pet/"
        self.sub_fix = "accept: application/json"
        self.pet_js_data = {}
        self.pet_data = '''
        {
          "id": 0,
          "category": {
            "id": 0,
            "name": "string"
          },
          "name": "doggie",
          "photoUrls": [
            "string"
          ],
          "tags": [
            {
              "id": 0,
              "name": "string"
            }
          ],
          "status": "available"
        }
        '''
        self.help = '''
    Pet Store Access From Swagger
        [Action]    <pet_name> <pet_id>
         get        Find pet with ID
         add        Add pet to the store
         delete     Delete pet from the store
         post       Update pet (name and/or ID)
    '''

    def load_pet_data(self):
        self.pet_js_data = json.loads(self.pet_data)
        self.pet_js_data['id'] = self.pet_id
        self.pet_js_data['name'] = self.pet_name

    def get(self):
        self.pet_js_data = sub.check_output(["curl", "-X", "GET", self.url, "-H", self.sub_fix])
        pet_data = json.loads(self.pet_js_data)
        if not 'name' in pet_data.keys():
            print(pet_data['message'])
        else:
            print("Pet name: {0}\nPet ID: {1}".format(pet_data['name'], pet_data['id']))

    def post(self):
        self.load_pet_data()
        curl_add = "curl -X PUT " + self.pre_url +\
                    " -H \"Content-Type: application/json\" -d " +\
                    "'{}'".format(json.dumps(self.pet_js_data))
        os.system(curl_add)

    def delete(self):
        sub.check_output(["curl", "-X", "DELETE", self.url, "-H", self.sub_fix])
    
    def add(self):
        self.load_pet_data()
        curl_add = "curl -X POST " + self.pre_url +\
                   " -H \"Content-Type: application/json\" -d " +\
                   "'{}'".format(json.dumps(self.pet_js_data))
        os.system(curl_add)

    def parse_cmd(self):
        self.main_action = sys.argv[1]

        parser = argparse.ArgumentParser(description="Pet store Actions", epilog="What's your pet?",
                                         usage=self.help)
        parser.add_argument("cmd", help="Actions with the pet")

        if self.main_action == "get":
            parser.add_argument("input", type=str, nargs=1,
                                help="Find the pet with pet ID and name")
        elif self.main_action == "add":
            parser.add_argument("input", type=str, nargs=2,
                                help="Add pet to the store")
        elif self.main_action == "delete":
            parser.add_argument("input", type=str, nargs=1,
                                help="Delete pet from the store")
        elif self.main_action == "post":
            parser.add_argument("input", type=str, nargs=2,
                                help="Update Pet ID and/or name")

        options = parser.parse_args()
        if self.main_action != "get" and self.main_action != "delete":
            self.pet_name, self.pet_id = options.input
        else:
            self.url = self.pre_url + ''.join(options.input)
        return getattr(self, self.main_action)()

    def run(self):
        try:
            self.parse_cmd()
        except IndexError:
            print pet.help
            sys.exit(1)

if __name__ == "__main__":
    pet = Pet()
    pet.run()