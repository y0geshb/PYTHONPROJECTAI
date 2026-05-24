import json
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


def load_response(file_path):

    absolute_path = os.path.join(
        BASE_DIR,
        file_path
    )

    print("Loading JSON from:", absolute_path)

    with open(absolute_path, "r", encoding="utf-8") as file:
        return json.load(file)