import json


def load_response(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)