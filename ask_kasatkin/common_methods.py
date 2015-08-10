# coding:utf8

import json

from best_parser import FILENAME

# this script loads data every time any page is requested from BROWSER!

def get_static_data():
    try:
        f = open(FILENAME, "r")
        data = json.loads(f.read())
        f.close()
        return data
    except:
        # if no file found ...
        return {
            "popular_users": [],
            "popular_tags": []
        }
