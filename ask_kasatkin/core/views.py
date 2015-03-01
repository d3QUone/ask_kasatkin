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
    demo_pop_tags = ["Technopark", "Baumanka", "C", "Python", "MySQL", "Ruby", "apple", "iOS", "swift", "django", "php", "flask",
                     "objective-c", "Ubuntu-server", "VPS", "Coffee Script", "sudo"]
    demo_labels = ["label label-default", "label label-primary", "label label-success",
                   "label label-info", "label label-warning", "label label-danger"]
    for tag in demo_pop_tags:
        append({"text": tag, "label": demo_labels[randint(0, len(demo_labels)-1)]})
    data["popular_users"] = ["Vasya Pupkin", "accl_9912_xz", "Dart Vader", "ggl.cm"]
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
    # - check & save
    '''
    login_ = request.POST['input_login']
    nickname_ = request.POST['input_nickname']
    email_ = request.POST['input_email']
    password1_ = request.POST['input_password']
    password2_ = request.POST['input_password_rep']
    '''
    # a) OK - create a new user, return main page
    # b) send an error msg, return the same page
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
