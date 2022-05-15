import json


class Convert:
    def __init__(self, json_file_name):
        self.json_conversions = Convert.load_json(json_file_name)

    def from_to(self, from_currency, to_currency):
        return from_currency in self.json_conversions['TO_' + to_currency]


    @staticmethod
    def load_json(json_file_name):
        with open(json_file_name) as json_file:
            json_file = json.load(json_file)
        return json_file
