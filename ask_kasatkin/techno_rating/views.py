# coding:utf8

import sys
reload(sys)
sys.setdefaultencoding('utf8') # make UTF 8 global-hack

from django.shortcuts import render
from techno_rating.models import TechIdea


def index(request):
    data = TechIdea.objects.all().order_by('-like')[:100]
    return render(request, "rating_page.html", {"data": data})
