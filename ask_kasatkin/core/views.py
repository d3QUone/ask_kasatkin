# coding:utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template import loader, RequestContext

from random import randint  # used in demo

# -- gets new questions, etc...
def index_page(request):
    # ------- A STATIC DEMO -------
    data = get_static_data()
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
        },
        {
            "title": "long-long title test | "*7,
            "link": "link_to_open_the_question_thread_by_ID_i_think",
            "text": "See the ModelForm documentation for more information. You should only need to call a model’s full_clean() method if you plan to handle validation errors yourself, or if you have excluded fields from the ModelForm that require validation."[:400] + "...",  # first 400 chars e.g
            # "date": "28.02.15 ",  # no data in block, needed for sorting only
            "rating": 341550,
            "answers": 200124,  # contributed answers
            "tags": ["Long tags are rather cool but not in Bootstrap :)", "Testing tempate with big footer", "noSQL is here"],  # 3 tags - MAX

            "author": "1335",
            "avatar": "1335.jpg"
        }
    ]
    # make sure the user is logged
    if request.user.is_authenticated():
        # load from model ...
        data["personal"] = {
            "nickname": "Vladimir",
            "avatar": "Vladimir.jpg"
        }
    return render(request, "core/templates/index.html", data)


# render login page
def show_login(request):
    return render(request, "core/templates/login.html", get_static_data())


# check input values + return main page back
def validate_login(request):
    data = get_static_data()
    if request.method == "POST":
        rec_login = request.POST["input_login"]
        rec_passw = request.POST["input_password"]
        if len(rec_login) == 0:
            data["error"] = {"title": "No login", "text": "Please enter your login and try again"}
        elif len(rec_passw) == 0:
            data["error"] = {"title": "No password", "text": "Please enter your password and try again"}
        else:
            # do login stuff ...
            user = authenticate(username=rec_login, password=rec_passw)
            if user: # - cool :)
                login(request, user)
                return index_page(request) #render(request, "core/templates/index.html", data)
            else:
                data["error"] = {"title": str(user), "text": "No such user"}
    else:
        data["error"] = {"title": "Wrong request", "text": "You should use POST-requests only to login"}
    # returns error message
    return render(request, "core/templates/login.html", data)


# render registration page
def register(request):
    return render(request, "core/templates/register.html", get_static_data())


# check input values + return info
def validate_register(request):
    data = get_static_data()
    if request.method == "POST":
        login_ = request.POST['input_login']
        nickname_ = request.POST['input_nickname']
        email_ = request.POST['input_email']
        password1_ = request.POST['input_password']
        password2_ = request.POST['input_password_rep']

        # a) check all fields are filled
        # b) work with file ...
        # c) OK - create a new user, return main page
        # d) send an error msg, return the same page

    else:
        data["error"] = {"title": "Wrong request", "text": "You should use POST-requests only to login"}
    # returns error message
    return render(request, "core/templates/register.html", data)


# -- shown only for logged users:
def self_logout(request):
    logout(request)
    return index_page(request)


def self_settings(request):
    if request.user.is_authenticated():
        return HttpResponse("settings page")
    else:
        # can't be so, but who knows ....
        return HttpResponse("-redirect to te main page!")


# future mock up
def search(request):
    return HttpResponse("JSON result ... ")



# -- ALL METHODS CALL THIS! (static demo now)

# returns popular tags from file ? cache
def get_static_data():
    res = []
    append = res.append
    demo_pop_tags = ["Technopark", "Baumanka", "C", "Python", "MySQL", "Ruby", "apple", "iOS", "swift", "django", "php", "flask",
                     "objective-c", "Ubuntu-server", "VPS", "Coffee Script", "sudo"]
    demo_labels = ["label label-default", "label label-primary", "label label-success",
                   "label label-info", "label label-warning", "label label-danger"]
    for tag in demo_pop_tags:
        append({"text": tag, "label": demo_labels[randint(0, len(demo_labels)-1)]})

    data = {}
    data["popular_tags"] = res
    data["popular_users"] = ["Vasya Pupkin", "accl_9912_xz", "Dart Vader", "ggl.cm"]
    return data
