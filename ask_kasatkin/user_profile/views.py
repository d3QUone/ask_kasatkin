# coding:utf8

# make UTF 8 global!
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.core.validators import validate_email, ValidationError
from django.db import IntegrityError
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from user_profile.models import UserProperties
from user_profile.forms import LoginForm, RegistrationForm, SettingsFrom
from common_methods import get_static_data
import uuid  # to generate unique file names


##### USER PERSONAL DATA main method #####

def get_user_data(request):
    data = {}
    if request.user.is_authenticated():
        prop = UserProperties.objects.get(user_id=request.user.id)
        data["id"] = request.user.id
        data["nickname"] = prop.nickname
        data["avatar"] = "{0}.jpg".format(prop.filename)  # don't forget to update extensions
    return data


# render login page - OK
@require_GET
def show_login(request):
    return render(request, "user_profile__login.html", get_static_data())


# check input values + return main page back
@require_POST
def validate_login(request):
    data = get_static_data()
    form = LoginForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        try:
            user = authenticate(username=data["login"], password=data["password"])
            login(request, user)
            return HttpResponsePermanentRedirect(reverse("core:home"))
        except AttributeError:
            data["error"] = {"title": "No such user", "text": "You can register this user"}
    else:
        data["error"] = form.errors.as_json()
    return render(request, "user_profile__login.html", data)


# render registration page - OK
@require_GET
def register(request):
    return render(request, "user_profile__register.html", get_static_data())


def save_avatar_by_id(f, user_id):
    # -- next step: get file extension with JS on frontend, save by correct extension
    filename = "{0}-{1}".format(user_id, uuid.uuid4())
    with open("uploads/{0}.jpg".format(filename), "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename


# check input values + return info - OK
@require_POST
def validate_register(request):
    data = get_static_data()
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
            data["error"] = {"error": ve.message}
        except IntegrityError:
            data["error"] = {"error": "That login is not free!"}
    else:
        data["error"] = form.errors.as_json()
    # returns error message
    data["personal"] = get_user_data(request)  # processes all user's-stuff
    return render(request, "user_profile__register.html", data)


# shown only for logged users - OK
@require_GET
def self_logout(request):
    logout(request)
    return HttpResponsePermanentRedirect(reverse("core:home"))


def self_settings(request, error=None):
    data = get_static_data()
    data["personal"] = get_user_data(request)  # processes all user's-stuff
    if error:
        data["error"] = error
    if request.user.is_authenticated(): # add email to other data
        user_id = request.user.id
        data["personal"]["email"] = User.objects.get(id=user_id).email
    return render(request, "user_profile__setting.html", data)


@require_POST
def update_settings(request):
    error = None
    if request.user.is_authenticated():
        #form = SettingsFrom(request.POST)  # do with forms...

        uid = request.user.id

        # update nickname if OK
        nickname_ = request.POST['input_nickname']
        if 5 <= len(nickname_) <= 20:
            UserProperties.objects.filter(user_id=uid).update(nickname=nickname_)
        elif len(nickname_) > 0:
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
            try:
                validate_email(email_)
                User.objects.filter(id=uid).update(email=email_)
            except ValidationError as ve:
                error = {"text": ve.message}  # + update templates to show errors in its fields
    else:
        error = {"title": "Auth error", "text": "Login and try once more please"}
    return self_settings(request, error=error)  # return the same page with new data
