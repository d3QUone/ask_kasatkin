# encoding: utf8

# make UTF 8 global!
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from core.models import user_properties, the_question, the_answer, the_tag, store_tag, likes_questions, likes_answers

from django.http import HttpResponse
from random import randint  # used in demo
from django.views.decorators.csrf import csrf_exempt  # reset csrf-checkup


# test method, HOME TASK 4
@csrf_exempt
def test(request):
    out = "Hello World<hr>\n"
    if request.method == "GET":
        for key in request.GET:
            out += "<strong>{0}:</strong> {1}<br>\n".format(key, request.GET[key])
    elif request.method == "POST":
        for key in request.POST:
            out += "<strong>{0}:</strong> {1}<br>\n".format(key, request.POST[key])
    return HttpResponse(out)


##### USER PERSONAL DATA (FOR LOGGED IN), main method #####

def get_user_data(request):
    data = {}
    if request.user.is_authenticated():
        user_id = request.user.id
        prop = user_properties.objects.get(user_id=user_id)
        data["nickname"] = prop.nickname
        data["avatar"] = "{0}.jpg".format(user_id)  # don't forget to update extensions
    return data


##### MAIN PAGE #####

# -- renders new questions, pagination
def index_page(request, offset = 0):
    data = get_static_data()
    data["personal"] = get_user_data(request)  # processes all user's-stuff

    Q_buffer = []
    append = Q_buffer.append

    Question_Data = the_question.objects.all().order_by('-date')[offset*30:(offset+1)*30]
    for item in Question_Data:

        #ans_count = the_answer.objects.get(contributed_to=item).count()

        append({
            "title": item.title,
            "text": item.text,
            "rating": item.rating,
            #"answers": ans_count, # <--- count related answers (the_answer)
            #"tags": item. , #-- get related (tags)

            "author": item.author,
            "avatar": "{0}.jpg".format(item.author.id),

            "question_id": item.id
        })

    data["questions"] = Q_buffer

    '''
    # ------- A STATIC DEMO -------
    data["questions"] = [
        {
            "title": "how to make a pretty block with css?",
            "text": "few text now to test",  # first 400 chars e.g
            "rating": -1,
            "answers": 1,  # contributed answers
            "tags": ["CSS3", "HTML5"],

            "author": "CSS_KILLER",
            "avatar": "demo_CSS_KILLER.jpg",  # img = author_ID + '.jpg'
            "question_id": 3
        },
        {
            "title": "what's wrong with my django-app urls?",
            "text": "When you use a ModelForm, the call to is_valid() will perform these validation steps for all the fields that are included on the form. See the ModelForm documentation for more information. You should only need to call a model’s full_clean() method if you plan to handle validation errors yourself, or if you have excluded fields from the ModelForm that require validation."[:400] + "...",  # first 400 chars e.g
            "rating": 3,
            "answers": 2,  # contributed answers
            "tags": ["Python", "Django", "MySQL"],  # 3 tags - MAX

            "author": "Vladimir",
            "avatar": "demo_Vladimir.jpg",
            "question_id": 2
        },
        {
            "title": "long-long title test | " * 7,
            "text": "See the ModelForm documentation for more information. You should only need to call a model’s full_clean() method if you plan to handle validation errors yourself, or if you have excluded fields from the ModelForm that require validation."[:400] + "...",  # first 400 chars e.g
            "rating": 341550,
            "answers": 200124,  # contributed answers
            "tags": ["Long tags are rather cool but not in Bootstrap :)", "Testing tempate with big footer",
                     "noSQL is here"],  # 3 tags - MAX

            "author": "1335",
            "avatar": "demo_1335.jpg",
            "question_id": 1
        }
    ]
    '''
    return render(request, "index.html", data)




#####

def prepare_question(question_id):
    # static demo as usual
    '''
    data = [
        {
            "title": "how to make a pretty block with css?",
            "text": "few text now to test",  # first 400 chars e.g
            "rating": -1,
            "answers": 1,  # contributed answers
            "tags": ["CSS3", "HTML5"],

            "author": "CSS_KILLER",
            "avatar": "demo_CSS_KILLER.jpg",  # img = author_ID + '.jpg'
            "question_id": 3
        },
        {
            "title": "what's wrong with my django-app urls?",
            "text": "When you use a ModelForm, the call to is_valid() will perform these validation steps for all the fields that are included on the form. See the ModelForm documentation for more information. You should only need to call a model’s full_clean() method if you plan to handle validation errors yourself, or if you have excluded fields from the ModelForm that require validation."[:400] + "...",  # first 400 chars e.g
            "rating": 3,
            "answers": 2,  # contributed answers
            "tags": ["Python", "Django", "MySQL"],  # 3 tags - MAX

            "author": "Vladimir",
            "avatar": "demo_Vladimir.jpg",
            "question_id": 2
        },
        {
            "title": "long-long title test | " * 7,
            "text": "See the ModelForm documentation for more information. You should only need to call a model’s full_clean() method if you plan to handle validation errors yourself, or if you have excluded fields from the ModelForm that require validation."[:400] + "...",  # first 400 chars e.g
            "rating": 341550,
            "answers": 200124,  # contributed answers
            "tags": ["Long tags are rather cool but not in Bootstrap :)", "Testing tempate with big footer",
                     "noSQL is here"],  # 3 tags - MAX

            "author": "1335",
            "avatar": "demo_1335.jpg",
            "question_id": 1
        }
    ]
    '''

    # load data from DB
    question = the_question.objects.get(id=question_id)

    # prepare
    data = {}
    data["title"] = question.title
    data["text"] = question.text
    data["rating"] = question.rating

    data["author"] = question.author
    data["avatar"] = "{0}.jpg".format(question.author.id)

    data["question_id"] = question_id
    return data


# shows a concrete thread: question + answers, allows logged in users add answers, vote
def question_thread(request, qid = 0):
    data = get_static_data()
    data["personal"] = get_user_data(request)

    # if 'qid' == 0 (means no id) return prepared page with helpful links on usage!
    # - e.g. how to register / add question / ...
    if qid == 0:
        data["question"] = {
            "title": "Use another ID :)"
        }
    else:
        # load question
        data["question"] = prepare_question(qid)
        data["answers"] = [
            {
                "text": "you better read reference on your theme man ;)... testing a <strong>leak</strong> inside STATIC-answer body....\n :) :) :)",
                "rating": 3,
                "selected": True,
                "author": "CSS_KILLER",
                "avatar": "demo_CSS_KILLER.jpg",
                "id": 1
            },
            {
                "text": "sorry I can't help you with this ,,ao1-0 soiw0mqw --m9  dso pshh apo d",
                "rating": -5,
                "selected": False,
                "author": "Dummy",
                "avatar": "demo_Dummy.jpg",
                "id": 3
            }
        ]

        # load answers

    return render(request, "question_thread.html", data)


##### USER METHODS #####

# render login page - OK
def show_login(request):
    return render(request, "login.html", get_static_data())


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
                data["error"] = {"title": "No such user / wrong password", "text": ""}
    else:
        data["error"] = {"title": "Wrong request", "text": "You should use POST-requests only to login"}
    # returns error message
    return render(request, "login.html", data)


# render registration page - OK
def register(request):
    return render(request, "register.html", get_static_data())


# validation used in registration
def validate_new_email(email):
    if len(email) > 4:
        return True
    else:
        return False


def save_avatar_by_id(f, user_id):
    # -- nex step -- get file extension with JS on frontend, save by correct extension
    # 'core/static/core/{0}.jpg' ---> 'uploads/{0}.jpg'
    with open('uploads/{0}.jpg'.format(user_id), 'wb+') as destination:
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
        try:
            avatar_file = request.FILES['avatar']
        except:
            avatar_file = request.POST['avatar']  # no file sent

        if len(login_) < 5:
            data["error"] = {"title": "Login-field", "text": "Please use login at least 5 symbols long"}
        elif len(nickname_) < 5:
            data["error"] = {"title": "Nickname-field", "text": "Please use nickname at least 5 symbols long"}
        elif len(password1_) < 5:
            data["error"] = {"title": "Password-field", "text": "Please use password at least 5 symbols long"}
        else:
            if validate_new_email(email_):
                if password1_ == password2_:
                    if len(avatar_file) > 0:
                        try:
                            user = User.objects.create_user(username=login_, email=email_, password=password1_)
                            user.save()
                            save_avatar_by_id(avatar_file, user.id)

                            props = user_properties()
                            props.user = user
                            props.nickname = nickname_
                            props.save()

                            # uncomment to return logged in user
                            user = authenticate(username=login_, password=password1_)
                            login(request, user)

                            return index_page(request)
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
    return render(request, "register.html", data)


# shown only for logged users - OK
def self_logout(request):
    logout(request)
    return index_page(request)


def self_settings(request, error = None):
    data = get_static_data()
    data["personal"] = get_user_data(request)  # processes all user's-stuff
    if error:
        data["error"] = error
    if request.user.is_authenticated(): # add email to other data
        user_id = request.user.id
        data["personal"]["email"] = User.objects.get(id=user_id).email
    return render(request, "setting.html", data)


def update_settings(request):
    error = None
    if request.method == "POST":
        if request.user.is_authenticated():
            uid = request.user.id
            # update nickname if OK
            nickname_ = request.POST['input_nickname']
            if len(nickname_) > 0:
                if len(nickname_) > 4:
                    props = user_properties.objects.get(user_id=uid)
                    props.nickname = nickname_
                    props.save()
                else:
                    error = {"title": "Your nickname must be at least 5 chars long", "text": ""}
            # upload new ava if any
            try:
                avatar_file = request.FILES['avatar']
                save_avatar_by_id(avatar_file, uid)
            except:
                pass
            # update email if OK
            email_ = request.POST['input_email']
            if len(email_) > 0:
                if validate_new_email(email_):
                    user = User.objects.get(id=uid)
                    user.email = email_
                    user.save()
                else:
                    error = {"title": "Incorrect email", "text": "Please use a valid email"}
        else:
            error = {"title": "Auth error", "text": "Login and try once more please"}
    return self_settings(request, error=error)  # return the same page with new data



##### QUESTIONS ######

# show add-new-question page
def new_question(request, error=None):
    data = get_static_data()
    data["personal"] = get_user_data(request)  # processes all user's-stuff
    data["error"] = error
    return render(request, "add_question.html", data)


# upload data and add question
def add_new_question(request):
    error = None
    if request.method == "POST":
        title = request.POST["title"]
        text = request.POST["text"]
        tags = request.POST["tags"].split(",")
        if len(title) < 10:
            error = {"title": "Too short title", "text": "Use at least 10 symbols in the title"}
        elif len(text) < 10:
            error = {"title": "Too short question", "text": "Describe your problem in a proper way please"}
        elif len(tags) > 3:
            error = {"title": "You can use only 3 tags", "text": "{0} tags were provided in new question".format(len(tags))}
        else:
            # - save to DB
            # - - think where to redirect back

            quest = the_question()
            quest.title = title[:250] # max 250 chars
            quest.text = text
            quest.author = request.user
            quest.save()

            '''
            # not related now...
            for t in tags[:3]:
                tag = the_tag()
                tag.name = str(t).lower()  # any lower?
                tag.save()

                # all tags stores in lower case
                #parent_tag = store_tag.objects.get(name=)
            '''

            error = {"title": "Saved OK", "text": ""}

    return new_question(request, error=error)



def add_new_answer(request):
    # process...


    # show the same page
    return question_thread(request, qid=0)


##### SEARCH #####

# !!! same template to search by tag OR by name
# even everything the same... different sources of data only
def search(request):
    return HttpResponse("JSON result ... ")



##### STATIC DATA #####

# returns popular tags from file ? cache, will be dynamic in future updates
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
