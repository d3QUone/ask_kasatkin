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

from user_profile.models import user_properties
from core.models import tag_name, store_tag
import json

FILENAME = "best_data.txt"

# I don't want to work with cron now.. so is will be manual now

# this script loads (?) once an hour, asks db for updates and save the results

# get TOP20 users - easy
def get_pop_users():
    result = []
    append = result.append
    for user_data in list(user_properties.objects.all().order_by('-rating')[:20]):
        append(user_data.nickname)
    return result


label_color = [
    "#DD4814", "#E05A2B", "#E36C43", "#E77E5A", "#EA9172",
    "#EEA389", "#EFAC95", "#F1B5A1", "#F3BEAC", "#F4C8B8",
    "#F6D1C4", "#F8DAD0", "#F9E3DB", "#FBECE7", "#FBECE7",
    "#FBECE7", "#FBECE7", "#FBECE7", "#FBECE7", "#FBECE7",
]

# get TOP20 tags here
def get_pop_tags():
    save = {}
    result = []
    append = result.append
    for tag in tag_name.objects.all():
        amount = store_tag.objects.filter(tag=tag).count()
        append(amount)
        save[amount] = tag.name
    result.sort(reverse=True)
    return [{"text": save[result[i]], "label": label_color[i]} for i in range(len(result[:20]))]


def save_data():
    data = {}
    data["popular_users"] = get_pop_users()
    data["popular_tags"] = get_pop_tags()
    with open(FILENAME, "w") as f:
        f.write(json.dumps(data))


save_data()  # run this stuff once

