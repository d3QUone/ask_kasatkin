#!/usr/bin/python

# 0) make UTF 8 global-hack

import sys
reload(sys)
sys.setdefaultencoding('utf8') 

# 1) import django

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ask_kasatkin.settings")
django.setup()

# 2) import models, etc else

from techno_rating.models import TechIdea
from bs4 import BeautifulSoup as bs
import requests

href_len = len('''href="''')

headers = {
    "User-agent": "Mozilla/5.0"
}

def parse_site():
    page = requests.get("http://techno-start.ru/ideas_top/", headers=headers)
    soup = bs(page.text)

    # get top ID (latest), load one by one then
    item = soup.find_all("div", "idea idea_bg-10")[0]
    a = str(item).find('''href="''')
    item = str(item)[a+href_len:]
    link = item[:item.find('"')]

    top_ID = int(link.split("/")[2])  # ['', 'idea', '8', '']
    for i in range(top_ID + 1):
        parse_content_by_id(i)


def parse_content_by_id(tech_id):
    page = requests.get("http://techno-start.ru/idea/{0}".format(tech_id), headers=headers)
    if page.status_code != 404:
        soup = bs(page.text)

        title = str(soup.find_all("div", "title title_left")[0].next)

        rating_block = soup.find_all("div", "actions")[0]
        like = int(rating_block.find_all("span", "link__title")[0].next)
        comm = int(rating_block.find_all("span", "link__title comments-cnt")[0].next.replace(" ", "").replace("\n", ""))

        try:
            idea = TechIdea.objects.get(tech_id=tech_id)
            idea.like = like
            idea.comm = comm
            idea.save()
            #TechIdea.objects.filter(tech_id=tech_id).update(like=like, comm=comm)  # doesn't hit when no object
        except TechIdea.DoesNotExist:
            TechIdea.objects.create(tech_id=tech_id, name=title, like=like, comm=comm)


if __name__ == "__main__":
    parse_site()
