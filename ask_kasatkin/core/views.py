# coding:utf8

# make UTF 8 global!
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from core.models import the_question, the_answer, store_tag, tag_name, likes_answers, likes_questions
from user_profile.models import user_properties
from user_profile.views import get_user_data
from common_methods import get_static_data
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt  # reset csrf-checkup, will use in AJAX
from django.http import HttpResponse    # jquery simple return
from random import randint  # used in demo


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


##### MAIN PAGE #####

# -- render question dict from DB-object
def create_question_item(item):
    amount = the_answer.objects.filter(contributed_to=item).count()
    prop = user_properties.objects.get(user_id=item.author.id)
    related_tags = store_tag.objects.filter(question=item)
    tags = [s_tag.tag.name for s_tag in related_tags]
    return {
        "question_id": item.id,
        "title": item.title,
        "text": item.text,
        "rating": item.rating,
        "answers": amount,
        "tags": tags,

        "author": item.author,
        "avatar": "{0}.jpg".format(prop.filename),
        "nickname": prop.nickname  # for render
    }


def index_page(request):
    if request.method == "GET":
        try:
            offset = int(request.GET["offset"])
        except:
            offset = 0
        try:
            query = request.GET["query"]
        except:
            query = "latest"

        if query != "popular":
            all_questions = the_question.objects.all().order_by('-date')[offset*30:(offset+1)*30]
        else:
            all_questions = the_question.objects.all().order_by('-rating')[offset*30:(offset+1)*30]

        # create data to render
        buf = []
        append = buf.append
        for item in all_questions:
            append(create_question_item(item))

        data = get_static_data()
        data["personal"] = get_user_data(request)  # processes all user's-stuff
        data["questions"] = buf
        data["offset"] = offset  # save request params to render page like a boss
        data["query"] = query
        return render(request, "core__index.html", data)



##### QUESTION THREAD #####

# shows a concrete thread: question + answers, allows logged in users add answers, vote
def question_thread(request, qid=0, error=None):
    # if 'qid' == 0 (means no id) return prepared page with helpful links on usage ???
    # e.g. how to register / add question / ???...
    if qid == 0:
        return index_page(request)
    else:
        data = get_static_data()
        data["personal"] = get_user_data(request)
        data["error"] = error
        question = the_question.objects.get(id=qid)
        data["question"] = create_question_item(question)
        if data["question"]["author"] == request.user:
            data["owner"] = True
        else:
            data["owner"] = False

        answers = the_answer.objects.filter(contributed_to=question)

        buf = []
        append = buf.append
        for a in answers:
            prop = user_properties.objects.get(user_id=a.author.id)  # load user properties
            append({
                "id": a.id,
                "text": a.text,
                "rating": a.rating,
                "selected": a.is_marked_as_true,

                "author": prop.nickname,
                "avatar": "{0}.jpg".format(prop.filename),
            })
        data["answers"] = buf
        return render(request, "core__question_page.html", data)



##### QUESTIONS ######

# show add-new-question page
def new_question(request, error=None):
    data = get_static_data()
    data["personal"] = get_user_data(request)  # processes all user's-stuff
    data["error"] = error
    return render(request, "core__ask.html", data)


# upload data and add question
def add_new_question(request):
    error = None
    if request.method == "POST" and request.user.is_authenticated():
        title = request.POST["title"]
        text = request.POST["text"]
        tags = request.POST["tags"].replace(" ", "").split(",")
        if len(title) < 10:
            error = {"title": "Too short title", "text": "Use at least 10 symbols in the title"}
        elif len(text) < 10:
            error = {"title": "Too short question", "text": "Describe your problem in a proper way please"}
        elif len(tags) > 3:
            error = {"title": "You can use only 3 tags", "text": "{0} tags were provided in new question".format(len(tags))}
        else:
            # - save to DB
            quest = the_question()
            quest.title = title[:250] # max 250 chars
            quest.text = text  # &lt;br&gt;
            quest.author = request.user
            quest.save()

            for t in tags[:3]:
                if len(t) > 0:
                    try:
                        # check if this name is already in Base
                        tn = tag_name.objects.get(name=str(t).lower())
                    except:
                        # create if none
                        tn = tag_name()
                        tn.name = str(t).lower()
                        tn.save()

                    new_tag = store_tag()
                    new_tag.question = quest
                    new_tag.tag = tn
                    new_tag.save()
            # returns new (clear) thread
            return question_thread(request, qid=quest.id)
    else:
        error = {"title": "You are not logged in", "text": ""}
    return new_question(request, error=error)


# adding-answer method
def add_new_answer(request):
    redirect_id = 0
    error = None
    if request.method == 'POST':
        redirect_id = request.POST["redirect_id"]
        text = request.POST["text"]

        if len(text) > 10:
            ques = the_question.objects.get(id=redirect_id)

            ans = the_answer()
            ans.text = text
            ans.author = request.user
            ans.contributed_to = ques
            ans.save()
        else:
            error = {"title": "Too short answer", "text": "Describe your idea in a proper way please"}

    # how to show the same page????
    return question_thread(request, qid=redirect_id, error=error)


##### TAGS ######

def all_by_tag(request, tag_n=None):
    data = get_static_data()
    data["personal"] = get_user_data(request)  # processes all user's-stuff
    data["tag"] = tag_n

    try:
        tag = tag_name.objects.get(name=tag_n)
        related_questions = store_tag.objects.filter(tag=tag)

        buf = []
        append = buf.append
        for item in related_questions:
            append(create_question_item(item.question))
        data["questions"] = buf
    except:
        data["questions"] = None

    return render(request, "core__by_tag.html", data)


##### AJAX (POST) methods #####

# !!! same template to search by tag OR by name
# even everything the same... different sources of data only
@csrf_exempt
def search(request):
    if request.method == "POST":
        return HttpResponse("JSON result ... ")


# this first ...
@csrf_exempt
def like_post(request):
    if request.method == "POST":
        if request.user.is_authenticated():
            try:
                pid = int(request.POST["id"])
                like_state = int(request.POST["like"])  # -1 / 1
                question = the_question.objects.get(id=pid)
                usr = request.user
            except:
                return HttpResponse("None")
            try:
                # load current-user like object
                like = likes_questions.objects.get(question=question, user=usr)  # get 1 curr state
                if abs(like.state + like_state) <= 1:
                    like.state += like_state
                    like.save()
                    # update global rating
                    question.rating += like_state
                    question.save()
            except:
                # create new like if no like
                like = likes_questions()
                like.user = usr
                like.question = question
                if abs(like_state) == 1:
                    like.state = like_state
                    like.save()
                    # update global rating
                    question.rating += like_state
                    question.save()
            question = the_question.objects.get(id=pid)
            return HttpResponse(question.rating)
    return HttpResponse(None)


@csrf_exempt
def like_answer(request):
    if request.method == "POST":
        if request.user.is_authenticated():
            try:
                aid = int(request.POST["id"])
                like_state = int(request.POST["like"])  # -1 / 1
                answer = the_answer.objects.get(id=aid)
                usr = request.user
            except:
                return HttpResponse("None")
            try:
                # load current-user like object
                like = likes_answers.objects.get(answer=answer, user=usr)  # get 1 curr state
                if abs(like.state + like_state) <= 1:
                    like.state += like_state
                    like.save()
                    # update global rating
                    answer.rating += like_state
                    answer.save()
            except:
                # create new like if no like
                like = likes_answers()
                like.user = usr
                like.answer = answer
                if abs(like_state) == 1:
                    like.state = like_state
                    like.save()
                    # update global rating
                    answer.rating += like_state
                    answer.save()
            answer = the_answer.objects.get(id=aid)
            return HttpResponse(answer.rating)
    return HttpResponse(None)


#
# some automatic for testing
#

from user_profile.views import create, select_random_user
from datetime import datetime
from uuid import uuid4


def create_random_question(amount):
    test_set = "{0}-test".format(datetime.now())
    for i in range(amount):
        user = select_random_user()
        if not user:
            user = create()

        # create question
        question = the_question()
        question.author = user
        question.title = test_set
        question.text = "Test question\n" + "\n".join([str(uuid4())*2 for i in range(11)])
        question.rating = randint(-100, 100)
        question.save()

        # add tags
        try:
            tn = tag_name.objects.get(name="test_set_{0}".format(i))
        except:
            # create if none
            tn = tag_name()
            tn.name = "test_set_{0}".format(i)
            tn.save()

        new_tag = store_tag()
        new_tag.question = question
        new_tag.tag = tn
        new_tag.save()

        # create answer
        how_much = int(randint(0, 6))
        create_random_answers(question.id, how_much)


def create_random_answers(question_id=None, amount=0):
    if question_id:
        for i in range(amount):
            user = select_random_user()
            if not user:
                user = create()

            ques = the_question.objects.get(id=question_id)

            ans = the_answer()
            ans.text = "Test answer\n" + "\n".join(["{0}) {1}".format(i, uuid4()) for i in range(5)])
            ans.author = user
            ans.contributed_to = ques
            ans.save()


def fill_base():
    for i in range(100):
        create()
    create_random_question(100)