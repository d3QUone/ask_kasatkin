# coding:utf8

# make UTF 8 global!
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from core.models import Question, Answer, StoreTag, TagName, LikesAnswers, LikesQuestions
from user_profile.models import UserProperties
from user_profile.views import get_user_data
from common_methods import get_static_data
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt  # reset csrf-checkup, will use in AJAX
from django.http import HttpResponse, Http404         # jquery simple return

from django.core.paginator import Paginator

@csrf_exempt  # works not as a usual decorator... one decorator for the whole page (all methods)

# test method, HOME TASK 4
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

# select related /
# prefetch related <- better

# edit that 'prerender'

# -- render question dict from DB-object
def create_question_item(item):
    amount = Answer.objects.filter(question=item).count()
    prop = UserProperties.objects.get(user_id=item.author.id)
    related_tags = StoreTag.objects.filter(question=item)
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


# we use paginator on Index, Question by tag and Search-result fields... - 3 similar blocks
def index_page(request):
    if request.method == "GET":
        try:
            page = int(request.GET["page"])
            # page = int(request.GET.get("page")) # returns None if no par sent
            if page < 1:
                page = 1
        except:
            page = 1

        try:
            query = request.GET["query"]
        except:
            query = "latest"

        if query != "popular":
            all_questions = Question.objects.all().order_by('-id')  # life hack :)
        else:
            all_questions = Question.objects.all().order_by('-rating')

        paginator = Paginator(all_questions, 30)
        try:
            questions_to_render = paginator.page(page)  # return all this data to render paginator only + buf(the same + even more data)
        except:
            questions_to_render = paginator.page(paginator.num_pages)

        buf = []
        append = buf.append
        for item in questions_to_render:
            append(create_question_item(item))

        data = get_static_data()
        data["personal"] = get_user_data(request)  # processes all user's-stuff
        data["questions"] = buf
        # paginator...
        data["page"] = page
        data["query"] = query
        data["paginator"] = questions_to_render
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
        question = Question.objects.get(id=qid)
        data["question"] = create_question_item(question)
        if data["question"]["author"] == request.user:
            data["owner"] = True
        else:
            data["owner"] = False

        try:
            page = int(request.GET["page"])
            if page < 1:
                page = 1
        except:
            page = 1

        # add pagination for answers here!
        paginator = Paginator(Answer.objects.filter(question=question), 30)
        try:
            ans_to_render = paginator.page(page)
        except:
            ans_to_render = paginator.page(paginator.num_pages)

        buf = []
        append = buf.append
        for a in ans_to_render:
            prop = UserProperties.objects.get(user_id=a.author.id)  # load user properties
            append({
                "id": a.id,
                "text": a.text,
                "rating": a.rating,
                "selected": a.is_marked_as_true,

                "author": prop.nickname,
                "avatar": "{0}.jpg".format(prop.filename),
            })
        data["answers"] = buf
        # paginator...
        data["page"] = page
        data["paginator"] = ans_to_render
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
            quest = Question.objects.create(title=title[:250], text=text, author=request.user)

            for t in tags[:3]:
                if len(t) > 0:
                    # get_or_create "style"
                    try:
                        tn = TagName.objects.get(name=str(t).lower())
                    except:
                        tn = TagName.objects.create(name=str(t).lower())

                    StoreTag.objects.create(question=quest, tag=tn)
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
            Answer.objects.create(text=text, author=request.user, question=Question.objects.get(id=redirect_id))

            # send mail to author here!!!

        else:
            error = {"title": "Too short answer", "text": "Describe your idea in a proper way please"}
    return question_thread(request, qid=redirect_id, error=error)


##### TAGS ######

def all_by_tag(request, tag_n=None):
    data = get_static_data()
    data["personal"] = get_user_data(request)  # processes all user's-stuff

    try:
        page = int(request.GET.get("page", "1"))
    except:
        raise Http404

    try:
        data["tag"] = tag_n
        tag = TagName.objects.get(name=tag_n)

        paginator = Paginator(StoreTag.objects.filter(tag=tag), 30)
        try:
            q_to_render = paginator.page(page)
        except:
            q_to_render = paginator.page(paginator.num_pages)

        buf = []
        append = buf.append
        for item in q_to_render:
            append(create_question_item(item.question))
        data["questions"] = buf
        data["page"] = page
        data["paginator"] = q_to_render
    except:
        data["questions"] = None
    return render(request, "core__by_tag.html", data)


##### jQuery-AJAX (POST) methods #####

# I'll use this for all searches..
#
# - add a page dividing results by tag / by question ???
#
def search(request):
    if request.method == "POST":
        input = request.POST["input"]
        # smth here ...

        return HttpResponse({"text": "JSON result ... "}, content_type="application/json")


def like_post(request):
    if request.method == "POST":
        if request.user.is_authenticated():
            try:
                pid = int(request.POST["id"])
                like_state = int(request.POST["like"])  # -1 / 1
                question = Question.objects.get(id=pid)
                usr = request.user
                usr_props = UserProperties.objects.get(user=usr)
            except ValueError:
                return HttpResponse("None")
            try:
                like = LikesQuestions.objects.get(question=question, user=usr)  # get 1 curr state
                if abs(like.state + like_state) <= 1:
                    LikesQuestions.objects.filter(question=question, user=usr).update(state=like.state+like_state)
                    Question.objects.filter(id=pid).update(rating=question.rating+like_state)
                    UserProperties.objects.filter(user=usr).update(rating=usr_props.rating+like_state)
            except:
                # create new like if no like
                if abs(like_state) == 1:
                    LikesQuestions.objects.create(user=usr, question=question, state=like_state)
                    Question.objects.filter(id=pid).update(rating=(question.rating+like_state))
                    UserProperties.objects.filter(user=usr).update(rating=(usr_props.rating+like_state))
            return HttpResponse(Question.objects.get(id=pid).rating)
    return HttpResponse(None)




# .... fix this after adding Loading-Form

def like_answer(request):
    if request.method == "POST":
        if request.user.is_authenticated():
            try:
                aid = int(request.POST["id"])
                like_state = int(request.POST["like"])  # -1 / 1
                answer = Answer.objects.get(id=aid)
                usr = request.user
            except:
                return HttpResponse("None")
            try:
                # load current-user like object
                like = LikesAnswers.objects.get(answer=answer, user=usr)  # get 1 curr state
                if abs(like.state + like_state) <= 1:
                    like.state += like_state
                    like.save()
                    # update global rating
                    answer.rating += like_state
                    answer.save()
            except:
                # create new like if no like
                like = LikesAnswers()
                like.user = usr
                like.answer = answer
                if abs(like_state) == 1:
                    like.state = like_state
                    like.save()
                    # update global rating
                    answer.rating += like_state
                    answer.save()
            answer = Answer.objects.get(id=aid)
            return HttpResponse(answer.rating)
    return HttpResponse(None)


# user profile ( 2 templates )

# - separate page with Stats
# - separate page with question-preview, answer-preview

def user_profile_stats(request):
    if request.user.is_authenticated():
        current_user = request.user

        profile = UserProperties.objects.get(user=current_user)
        # get avatar, get rating...

        total_questions = Question.objects.filter(author=current_user).count()
        total_answers = Answer.objects.filter(author=current_user).count()

        data = {}
        data["profile"] = profile
        data["total_questions"] = total_questions
        data["total_answers"] = total_answers

        return render(request, "core__user_profile.html", data)

    return None


def user_profile_all_data(request):


    # paginator for all questions / or separate page with all questions and all answers
    return None