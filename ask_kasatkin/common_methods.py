from best_parser import FILENAME
import json

# this script loads data every time any page is requested from BROWSER!

def get_static_data():
    with open(FILENAME, "r") as f:
        data = json.loads(f.read())
        return data
