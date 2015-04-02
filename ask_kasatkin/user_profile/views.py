# coding:utf8

# make UTF 8 global!
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from user_profile.models import UserProperties
from common_methods import get_static_data

import uuid  # to generate unique filenames


##### USER PERSONAL DATA main method #####

def get_user_data(request):
    data = {}
    if request.user.is_authenticated():
        user_id = request.user.id
        prop = UserProperties.objects.get(user_id=user_id)
        data["nickname"] = prop.nickname
        data["avatar"] = "{0}.jpg".format(prop.filename)  # don't forget to update extensions
    return data


# render login page - OK
def show_login(request):
    return render(request, "user_profile__login.html", get_static_data())


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
                return HttpResponsePermanentRedirect(reverse("core:home"))
            else:
                data["error"] = {"title": "No such user / wrong password", "text": ""}
    else:
        data["error"] = {"title": "Wrong request", "text": "You should use POST-requests only to login"}
    # returns error message
    return render(request, "user_profile__login.html", data)


# render registration page - OK
def register(request):
    return render(request, "user_profile__register.html", get_static_data())


# validation used in registration
def validate_new_email(email):
    if len(email) > 5:
        ap = 0
        for ch in email:
            if ch == "@":
                ap += 1
            if ap > 1:
                return False
        return True
    return False


def save_avatar_by_id(f, user_id):
    # -- next step: get file extension with JS on frontend, save by correct extension
    filename = "{0}-{1}".format(user_id, uuid.uuid4())
    with open("uploads/{0}.jpg".format(filename), "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename


# check input values + return info - OK
def validate_register(request):
    data = get_static_data()
    if request.method == "POST":
        login_ = request.POST['input_login']
        nickname_ = request.POST['input_nickname']
        email_ = request.POST['input_email']
        password1_ = request.POST['input_password']
        password2_ = request.POST['input_password_rep']
        try:
            avatar_file = request.FILES['avatar']
        except:
            avatar_file = request.POST['avatar']  # no file sent

        if len(login_) < 5 or len(login_) > 30:
            data["error"] = {"title": "Login-field", "text": "Please use login at least 5 chars long and less then 30 chars"}
        elif len(nickname_) < 5 or len(nickname_) > 20:
            data["error"] = {"title": "Nickname-field", "text": "Please use nickname at least 5 chars long and less then 20 chars"}
        elif len(password1_) < 5:
            data["error"] = {"title": "Password-field", "text": "Please use password at least 5 symbols long"}
        else:
            if validate_new_email(email_):
                if password1_ == password2_:
                    if len(avatar_file) > 0:
                        try:
                            user = User.objects.create_user(username=login_, email=email_, password=password1_)
                            user.save()
                            filename_ = save_avatar_by_id(avatar_file, user.id)

                            UserProperties.objects.create(user=user, nickname=nickname_, filename=filename_)

                            # uncomment to return logged in user
                            user = authenticate(username=login_, password=password1_)
                            login(request, user)
                            return HttpResponsePermanentRedirect(reverse("core:home"))
                        except Exception as ex:
                            data["error"] = {"title": "Internal server error", "text": str(ex)}
                    else:
                        data["error"] = {"title": "No avatar", "text": "Avatar is required to create new account"}
                else:
                    data["error"] = {"title": "Passwords don't match",
                                     "text": "Please be careful on typing your password"}
            else:
                data["error"] = {"title": "Incorrect email", "text": "Please use a valid email"}
    else:
        data["error"] = {"title": "Wrong request", "text": "You should use POST-requests only to login"}
    # returns error message
    data["personal"] = get_user_data(request)  # processes all user's-stuff
    return render(request, "user_profile__register.html", data)


# shown only for logged users - OK
def self_logout(request):
    logout(request)
    return HttpResponsePermanentRedirect(reverse("core:home"))


def self_settings(request, error = None):
    data = get_static_data()
    data["personal"] = get_user_data(request)  # processes all user's-stuff
    if error:
        data["error"] = error
    if request.user.is_authenticated(): # add email to other data
        user_id = request.user.id
        data["personal"]["email"] = User.objects.get(id=user_id).email
    return render(request, "user_profile__setting.html", data)


def update_settings(request):
    error = None
    if request.method == "POST":
        if request.user.is_authenticated():
            uid = request.user.id

            # update nickname if OK
            nickname_ = request.POST['input_nickname']
            if len(nickname_) > 0:
                if len(nickname_) >= 5 and len(nickname_) <= 20:
                    UserProperties.objects.filter(user_id=uid).update(nickname=nickname_)
                else:
                    error = {"title": "Your nickname must be at least 5 chars long and less then 20 chars", "text": ""}

            # upload new ava if any
            try:
                avatar_file = request.FILES['avatar']
                # will exit condition if no file
                filename_ = save_avatar_by_id(avatar_file, uid)
                UserProperties.objects.filter(user_id=uid).update(filename=filename_)
            except:
                pass

            # update email if OK
            email_ = request.POST['input_email']
            if len(email_) > 0:
                if validate_new_email(email_):
                    User.objects.filter(id=uid).update(email=email_)
                else:
                    error = {"title": "Incorrect email", "text": "Please use a valid email"}
        else:
            error = {"title": "Auth error", "text": "Login and try once more please"}
    return self_settings(request, error=error)  # return the same page with new data
