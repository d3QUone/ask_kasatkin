# coding:utf8

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import uuid  # to generate unique file names
from datetime import datetime as dtime

from django.db import IntegrityError
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.validators import validate_email, ValidationError
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from ask_kasatkin.settings import BASE_DIR
from user_profile.models import UserProperties
from user_profile.forms import LoginForm, RegistrationForm
from common_methods import get_static_data


# TODO: add good 'help-page' with info on Russian and English + add footer

# TODO: add restore/reset-password-page


##### USER PERSONAL DATA main method #####

def get_user_data(request):
    data = {}
    if request.user.is_authenticated():
        prop = UserProperties.objects.get(user_id=request.user.id)
        data["id"] = request.user.id
        data["nickname"] = prop.nickname
        data["avatar"] = prop.filename
    return data


# GET -> render login page
# POST -> process input-form
def do_login(request):
    data = get_static_data()
    if not request.user.is_authenticated():
        if request.method == "POST":
            form = LoginForm(request.POST or None)
            if form.is_valid():
                try:
                    User.objects.get(username=form.cleaned_data["login"])  # just to ensure we have this user
                    user = authenticate(username=form.cleaned_data["login"], password=form.cleaned_data["password"])
                    if user:  # so the password is valid
                        login(request, user)
                        return HttpResponsePermanentRedirect(reverse("core:home"))
                    else:
                        data["form"] = {"no_user": "Wrong password!"}
                except User.DoesNotExist:
                    data["form"] = {"no_user": "No such user. You can register this user"}
            else:
                data["form"] = form
        return render(request, "user_profile__login.html", data)
    else:
        return HttpResponsePermanentRedirect(reverse("core:home"))


def save_avatar_by_id(f, user_id):
    date = dtime.now()

    # use 'os.path' for building paths
    folder_name = "{0}-{1}-{2}".format(date.year, date.month, date.day)
    directory = "{0}/uploads/{1}".format(BASE_DIR, folder_name)

    # catch is-exists exception
    if not os.path.isdir(directory):
        os.makedirs(directory)

    # add reading extensions from raw file (first 2 bytes)
    filename = "{0}/{1}-{2}.jpg".format(folder_name, user_id, uuid.uuid4())
    with open(BASE_DIR + "/uploads/" + filename, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename


# GET -> render registration page
# POST -> process input-form
def register(request):
    data = get_static_data()
    if not request.user.is_authenticated():
        if request.method == "POST":
            form = RegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                login_ = data['input_login']
                nickname_ = data['input_nickname']
                email_ = data['input_email']
                password_ = data['input_password']
                avatar_file = data['avatar']
                try:
                    validate_email(email_)
                    user = User.objects.create_user(username=login_, email=email_, password=password_)

                    filename_ = save_avatar_by_id(avatar_file, user.id)
                    UserProperties.objects.create(user=user, nickname=nickname_, filename=filename_)

                    user = authenticate(username=login_, password=password_)
                    login(request, user)
                    return HttpResponsePermanentRedirect(reverse("core:home"))
                except ValidationError as ve:
                    data["form"] = {"error": ve.message}
                except IntegrityError:  # user = User.objects.get(username=data["login"])  # is dat good?
                    data["form"] = {"error": "That login is not free!"}
            else:
                data["form"] = form
            data["personal"] = get_user_data(request)  # processes all user's-stuff
        return render(request, "user_profile__register.html", data)
    else:
        return HttpResponsePermanentRedirect(reverse("core:home"))


# only for logged users - OK
@require_POST
def do_logout(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponsePermanentRedirect(reverse("core:home"))


def self_settings(request):
    data = get_static_data()
    if request.user.is_authenticated():
        user_id = request.user.id
        if request.method == "POST":

            # update nickname if OK
            nickname_ = request.POST['input_nickname']
            if 5 <= len(nickname_) <= 20:
                UserProperties.objects.filter(user_id=user_id).update(nickname=nickname_)
            elif len(nickname_) > 0:
                data["error"] = {"title": "Your nickname must be at least 5 chars long and less then 20 chars", "text": ""}

            # upload new ava if any
            try:
                avatar_file = request.FILES['avatar']
                filename_ = save_avatar_by_id(avatar_file, user_id)
                UserProperties.objects.filter(user_id=user_id).update(filename=filename_)
            except KeyError:
                # no File in the dict
                pass

            # update email if OK
            email_ = request.POST['input_email']
            if len(email_) > 0:
                try:
                    validate_email(email_)
                    User.objects.filter(id=user_id).update(email=email_)
                except ValidationError as ve:
                    data["error"] = {"text": ve.message}  # + update templates to show errors in its fields

        data["personal"] = get_user_data(request)  # processes all user's-stuff
        data["personal"]["email"] = User.objects.get(id=user_id).email
    return render(request, "user_profile__setting.html", data)
