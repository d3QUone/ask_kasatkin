# coding:utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template import loader, RequestContext

from random import randint  # used in demo

# -- main page methods:
def index_page(request):
    # ------- A STATIC DEMO -------
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
    data["questions"] = [
        {
            "title": "how to make a pretty block with css?",
            "link": "link_to_open_the_question_thread_by_ID_i_think",
            "text": "few text now to test",  # first 400 chars e.g
            # "date": "28.02.15 ",  # no data in block, needed for sorting only
            "rating": -1,
            "answers": 1,  # contributed answers
            "tags": ["CSS3", "HTML5"],

            "author": "CSS_KILLER",
            "avatar": "CSS_KILLER.jpg"  # img = author + '.jpg'
        },
        {
            "title": "what's wrong with my django-app urls?",
            "link": "link_to_open_the_question_thread_by_ID_i_think",
            "text": "When you use a ModelForm, the call to is_valid() will perform these validation steps for all the fields that are included on the form. See the ModelForm documentation for more information. You should only need to call a model’s full_clean() method if you plan to handle validation errors yourself, or if you have excluded fields from the ModelForm that require validation."[:400] + "...",  # first 400 chars e.g
            # "date": "28.02.15 ",  # no data in block, needed for sorting only
            "rating": 3,
            "answers": 2,  # contributed answers
            "tags": ["Python", "Django", "MySQL"],  # 3 tags - MAX

            "author": "Vladimir",
            "avatar": "Vladimir.jpg"
        }
    ]
    # make sure the user is logged + load personal data
    if request.user.is_authenticated():
        data["personal"] = {
            "nickname": "Vladimir",
            "avatar": "Vladimir.jpg"
        }
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
