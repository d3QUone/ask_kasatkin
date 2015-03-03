# coding:utf8
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import user_properties

from django.http import HttpResponse
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
            "rating": -1,
            "answers": 1,  # contributed answers
            "tags": ["CSS3", "HTML5"],

            "author": "CSS_KILLER",
            "avatar": "CSS_KILLER.jpg"  # img = author_ID + '.jpg'
        },
        {
            "title": "what's wrong with my django-app urls?",
            "link": "link_to_open_the_question_thread_by_ID_i_think",
            "text": "When you use a ModelForm, the call to is_valid() will perform these validation steps for all the fields that are included on the form. See the ModelForm documentation for more information. You should only need to call a model’s full_clean() method if you plan to handle validation errors yourself, or if you have excluded fields from the ModelForm that require validation."[:400] + "...",  # first 400 chars e.g
            "rating": 3,
            "answers": 2,  # contributed answers
            "tags": ["Python", "Django", "MySQL"],  # 3 tags - MAX

            "author": "Vladimir",
            "avatar": "Vladimir.jpg"
        },
        {
            "title": "long-long title test | " * 7,
            "link": "link_to_open_the_question_thread_by_ID_i_think",
            "text": "See the ModelForm documentation for more information. You should only need to call a model’s full_clean() method if you plan to handle validation errors yourself, or if you have excluded fields from the ModelForm that require validation."[:400] + "...",  # first 400 chars e.g
            "rating": 341550,
            "answers": 200124,  # contributed answers
            "tags": ["Long tags are rather cool but not in Bootstrap :)", "Testing tempate with big footer",
                     "noSQL is here"],  # 3 tags - MAX

            "author": "1335",
            "avatar": "1335.jpg"
        }
    ]
    # make sure the user is logged:
    if request.user.is_authenticated():
        # get ID, ask properties by ID
        user_id = request.user.id
        prop = user_properties.objects.get(user_id=user_id)
        data["personal"] = {
            "nickname": prop.nickname,
            "avatar": str(user_id) + ".jpg"
        }
    return render(request, "core/templates/index.html", data)


# render login page - OK
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
            user = authenticate(username=rec_login, password=rec_passw)
            if user:
                login(request, user)
                return index_page(request)
            else:
                data["error"] = {"title": "No such user", "text": ""}
    else:
        data["error"] = {"title": "Wrong request", "text": "You should use POST-requests only to login"}
    # returns error message
    return render(request, "core/templates/login.html", data)


# render registration page - OK
def register(request):
    return render(request, "core/templates/register.html", get_static_data())


# validation used in registration
def validate_new_email(email):
    if len(email) > 4:
        return True
    else:
        return False


def save_avatar_by_id(f, user_id):
    # -- nex step -- get file extension with JS on frontend, save by correct extension
    with open('core/static/core/{0}.jpg'.format(user_id), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# check input values + return info - OK
def validate_register(request):
    data = get_static_data()
    if request.method == "POST":
        login_ = request.POST['input_login']
        nickname_ = request.POST['input_nickname']
        email_ = request.POST['input_email']
        password1_ = request.POST['input_password']
        password2_ = request.POST['input_password_rep']
        avatar_file = request.FILES['avatar']

        if len(login_) < 5:
            data["error"] = {"title": "Login-field", "text": "Please use login at least 5 symbols long"}
        elif len(nickname_) < 5:
            data["error"] = {"title": "Nickname-field", "text": "Please use nickname at least 5 symbols long"}
        elif len(password1_) < 5:
            data["error"] = {"title": "Password-field", "text": "Please use password at least 5 symbols long"}
        else:
            if validate_new_email(email_):
                if password1_ == password2_:
                    try:
                        user = User.objects.create_user(username=login_, email=email_, password=password1_)
                        user.save()
                        save_avatar_by_id(avatar_file, user.id)

                        props = user_properties()
                        props.user = user
                        props.nickname = nickname_
                        props.save()

                        '''
                        # uncomment to return logged in user
                        user = authenticate(username=login_, password=password1_)
                        login(request, user)
                        '''
                        return index_page(request)
                    except Exception as ex:
                        data["error"] = {"title": "Internal server error", "text": str(ex)}
                else:
                    data["error"] = {"title": "Passwords don't match",
                                     "text": "Please be careful on typing your password"}
            else:
                data["error"] = {"title": "Incorrect email", "text": "Please use a valid email"}
    else:
        data["error"] = {"title": "Wrong request", "text": "You should use POST-requests only to login"}
    # returns error message
    return render(request, "core/templates/register.html", data)


# shown only for logged users - OK
def self_logout(request):
    logout(request)
    return index_page(request)


def self_settings(request):
    if request.user.is_authenticated():
        return HttpResponse("settings page")
    else:
        return index_page(request)


def new_question(request):
    return HttpResponse("show add new question form")


def add_new_question(request):
    return HttpResponse("recieve and process data")


# future mock up
def search(request):
    return HttpResponse("JSON result ... ")



# returns popular tags from file ? cache
def get_static_data():
    res = []
    append = res.append
    demo_pop_tags = ["Technopark", "Baumanka", "C", "Python", "MySQL", "Ruby", "apple", "iOS", "swift", "django",
                     "php", "flask", "objective-c", "Ubuntu-server", "VPS", "Coffee Script", "sudo"]
    demo_labels = ["label label-default", "label label-primary", "label label-success",
                   "label label-info", "label label-warning", "label label-danger"]
    for tag in demo_pop_tags:
        append({"text": tag, "label": demo_labels[randint(0, len(demo_labels)-1)]})

    data = {}
    data["popular_tags"] = res
    data["popular_users"] = ["Vasya Pupkin", "accl_9912_xz", "Dart Vader", "ggl.cm", "qwerTY"]
    return data
