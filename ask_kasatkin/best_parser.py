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

from django.utils import timezone
from datetime import timedelta
from user_profile.models import UserProperties
from core.models import TagName, Question, Answer
import json

FILENAME = "best_data.txt"  # for output

# this script loads every 15 min, asks db for updates and save the results

# get TOP10 users !!! which questions and answers are most popular this week !!!
def get_pop_users():
    result = []
    append = result.append

    time_window = timezone.now() - timedelta(days=7)

    for best in list(Question.objects.filter(date__gte=time_window).order_by("-rating").prefetch_related("author")[:20]):
        buf = {
            "rating": best.rating,
            "nickname": best.author.nickname,
            "id": best.author.user.id
        }
        if buf not in result:
            append(buf)

    for best in list(Answer.objects.filter(date__gte=time_window).order_by("-rating").prefetch_related("author")[:20]):
        buf = {
            "rating": best.rating,
            "nickname": best.author.nickname,
            "id": best.author.user.id
        }
        if buf not in result:
            append(buf)

    result.sort()

    output = []
    append = output.append
    for usr in result:
        buf = {
            "nickname": usr["nickname"],
            "id": usr["id"]
        }
        if buf not in output:
            append(buf)
        if len(output) == 10:
            break
    return output


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
