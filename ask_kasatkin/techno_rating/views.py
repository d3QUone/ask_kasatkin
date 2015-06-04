# coding:utf8

import sys
reload(sys)
sys.setdefaultencoding('utf8') # make UTF 8 global-hack

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from techno_rating.models import TechIdea


def index(request):
    try:
        page = int(request.GET.get("page", "1"))
    except ValueError:
        raise Http404

    query = request.GET.get("sort", "latest")
    if query != "popular":
        paginator = Paginator(TechIdea.objects.all().order_by('-id'), 30)
    else:
        paginator = Paginator(TechIdea.objects.all().order_by('-like'), 30)

    try:
        data = paginator.page(page)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    return render(request, "rating_page.html", {"data": data})
