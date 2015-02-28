from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template import loader, RequestContext

from random import randint

# -- main page methods:
def index_page(request):
    # demonstation
    data = {}
    data["popular_tags"] = []
    append = data["popular_tags"].append
    demo_pop_tags = ["Python", "MySQL", "Ruby", "apple", "iOS", "swift", "django", "php", "flask",
                     "objective-c", "Ubuntu-server", "VPS", "Coffee Script", "sudo"]
    demo_labels = ["label label-default", "label label-primary", "label label-success",
                   "label label-info", "label label-warning", "label label-danger"]
    for tag in demo_pop_tags:
        append({"text": tag, "label": demo_labels[randint(0, len(demo_labels)-1)]})
    data["questions"] = []
    # make sure the user is logged
    if request.user.is_authenticated():
        data["logged"] = True
    else:
        data["logged"] = False
        # if not - render actually only the other page header
    return render(request, "core/templates/index.html", data)


# returns main page back
def log_in(request):
    # - pop-up was in frontend
    # - gets data from POST (from index_page), login
    return render(request, "core/templates/index.html")


# simple return
def register(request):
    return render(request, "core/templates/register.html")


def validate_registration(request):
    # - get data
    # - check & save, redirect OR send an error msg
    return HttpResponse("render main page after successful registration")


# -- shown only for loged users:
def self_logout(request):
    logout(request)
    return HttpResponse("logout OK + link to success message")


def self_settings(request):
    if request.user.is_authenticated():
        return HttpResponse("settings page")
    else:
        # can't be so, but who knows ....
        return HttpResponse("-redirect to te main page!")
