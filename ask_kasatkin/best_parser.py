#!/usr/bin/python
# coding:utf8

#
# script for creating the popular-set
#
# >> python best_parser.py
#

# 1) import django

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ask_kasatkin.settings")
django.setup()

# 2) import models, etc else

from user_profile.models import UserProperties
from core.models import TagName, Question
import json

FILENAME = "best_data.txt"  # for output

# this script loads (?) once an hour, asks db for updates and save the results

# get TOP20 users - easy
def get_pop_users():
    result = []
    append = result.append
    for user_data in list(UserProperties.objects.all().order_by('-rating')[:20]):
        append({
            "nickname": user_data.nickname,
            "id": user_data.user.id
        })
    return result


label_color = [
    "#DD4814", "#E05A2B", "#E36C43", "#E77E5A", "#EA9172",
    "#EEA389", "#EFAC95", "#F1B5A1", "#F3BEAC", "#F4C8B8",
    "#F6D1C4", "#F8DAD0", "#F9E3DB", "#FBECE7", "#FBECE7",
    "#FBECE7", "#FBECE7", "#FBECE7", "#FBECE7", "#FBECE7",
]


# get TOP20 tags here
def get_pop_tags():
    result = []
    append = result.append
    for tag in list(TagName.objects.all()):
        amount = Question.objects.filter(tags=tag).count()
        append([amount, tag.name])
    result.sort(reverse=True)
    return [{"text": result[i][1], "label": label_color[i]} for i in range(len(result[:20]))]


def save_data():
    data = {}
    data["popular_users"] = get_pop_users()
    data["popular_tags"] = get_pop_tags()
    with open(FILENAME, "w") as f:
        f.write(json.dumps(data))

if __name__ == "__main__":
    save_data()
