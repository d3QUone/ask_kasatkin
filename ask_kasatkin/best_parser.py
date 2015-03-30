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
from core.models import store_tag, the_question, the_answer
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


# get TOP20 tags here
def get_pop_tags():
    big_big_set = store_tag.objects.all()

    result = []
    append = result.append

    return result



def save_data():
    data = {}
    data["popular_users"] = get_pop_users()
    data["popular_tags"] = get_pop_tags()
    with open(FILENAME, "w") as f:
        f.write(json.dumps(data))


#demo_labels = ["label label-default", "label label-primary", "label label-success", "label label-info", "label label-warning", "label label-danger"]
#selected_tags = ["technopark", "baumanka", "c", "python", "mysql", "ruby", "apple", "iOS", "swift", "django", "sudo", "flask"]

save_data() # run this stuff once

