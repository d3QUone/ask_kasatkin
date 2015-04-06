# coding:utf8

import sys
reload(sys)
sys.setdefaultencoding('utf8') # make UTF 8 global-hack

from core.models import Question, Answer, TagName, Like
from core.forms import Like, NewQuestion, NewAnswer
from user_profile.models import UserProperties
from user_profile.views import get_user_data
from common_methods import get_static_data
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt  # reset csrf-checkup, will use in AJAX
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse, Http404         # jquery simple return
from django.core.paginator import Paginator


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

# we use paginator on Index, Question by tag and Search-result fields... - 3 similar blocks
def index_page(request):
    try:
        page = int(request.GET["page"])
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    try:
        query = request.GET["query"]
    except KeyError:
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

    data = get_static_data()
    data["personal"] = get_user_data(request)  # processes all user's-stuff
    data["page"] = page
    data["query"] = query
    data["paginator"] = questions_to_render   # TODO: in template: change all list objects name to 'paginator' + load related objects there
    return render(request, "core__index.html", data)


##### QUESTION THREAD #####

# shows a concrete thread: question + answers, allows logged in users add answers, vote
def question_thread(request, qid=0, error=None):
    if qid != 0:
        try:
            question = Question.objects.get(id=qid)
        except Question.DoesNotExist:
            raise Http404

        data = get_static_data()
        data["personal"] = get_user_data(request)
        data["error"] = error
        data["question"] = question
        if question.author.user == request.user:
            data["owner"] = True
        else:
            data["owner"] = False

        try:
            page = int(request.GET["page"])
            if page < 1:
                page = 1
        except KeyError:
            page = 1

        # add pagination for answers here!
        paginator = Paginator(question.answers.all(), 30)
        try:
            ans_to_render = paginator.page(page)
        except:
            ans_to_render = paginator.page(paginator.num_pages)

        '''
        buf = []
        append = buf.append
        for a in ans_to_render:
            prop = UserProperties.objects.get(user_id=a.author.id)  # load user properties
            append({
                "id": a.id,
                "text": a.text,
                "rating": a.rating,
                "selected": a.chosen,

                "author": prop.nickname,
                "avatar": "{0}.jpg".format(prop.filename),
            })
        data["answers"] = buf
        '''

        # paginator...
        data["page"] = page
        data["paginator"] = ans_to_render
        return render(request, "core__question_page.html", data)
    else:
        # we can show some prepared hint-pages in such cases e.g. how to register / add question / ...
        return index_page(request)


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
    if request.user.is_authenticated():
        form = NewQuestion(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            title = data["title"]
            text = data["text"]
            tags = data["tags"].replace(" ", "").split(",")

            quest = Question.objects.create(title=title[:250], text=text, author=request.user)
            for t in tags[:3]:
                if len(t) > 0:
                    # get_or_create "style"
                    try:
                        tn = TagName.objects.get(name=str(t).lower())
                    except TagName.DoesNotExist:
                        tn = TagName.objects.create(name=str(t).lower())
                    quest.tags.add(tn)
            return question_thread(request, qid=quest.id)
        else:
            error = form.errors.as_json()
    else:
        error = {"title": "You are not logged in", "text": ""}
    return new_question(request, error=error)


# adding-answer method
def add_new_answer(request):
    error = None
    form = NewAnswer(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        redirect_id = data["redirect_id"]
        text = data["text"]

        new_answer = Answer.objects.create(text=text, author=request.user)
        question = Question.objects.get(id=redirect_id)
        question.answers.add(new_answer)

        # TODO: send mail to question-author about added answer
    else:
        redirect_id = request.POST["redirect_id"]
        error = form.errors.as_json()
    return question_thread(request, qid=redirect_id, error=error)


# TODO: add mark-as-true method!!!


##### TAGS ######
@require_GET
def all_by_tag(request, tag_n=None):
    data = get_static_data()
    data["personal"] = get_user_data(request)  # processes all user's-stuff

    try:
        page = int(request.GET.get("page", "1"))
    except ValueError:
        raise Http404
    try:
        data["tag"] = tag_n
        paginator = Paginator(TagName.objects.get(name=tag_n), 30)

        try:
            q_to_render = paginator.page(page)
        except:
            q_to_render = paginator.page(paginator.num_pages)  # TODO: find paginator error names

        data["page"] = page
        data["paginator"] = q_to_render
    except:
        data["questions"] = None
    return render(request, "core__by_tag.html", data)



##### USER PROFILE (additional feature) #####

# - separate page for Stats
# - separate page for question-preview, answer-preview
@require_GET
def user_profile_stats(request, id=None):
    data = get_static_data()
    data["personal"] = get_user_data(request)
    if id:
        try:
            current_user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404
        data["profile"] = UserProperties.objects.get(user=current_user)
        data["total_questions"] = Question.objects.filter(author=current_user).count()
        data["total_answers"] = Answer.objects.filter(author=current_user).count()
    else:
        data["error"] = "No profile selected :("
    return render(request, "core__user_stats.html", data)


@require_GET
def user_profile_all_data(request):

    # paginator for all questions / or separate page with all questions and all answers
    return None


##### jQuery-AJAX (POST) methods #####

@csrf_exempt
@require_POST
def like_post(request):
    if request.user.is_authenticated():
        form = Like(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            pid = data["id"]
            like_state = data["like"]
            try:
                question = Question.objects.get(id=pid)
                author_account = UserProperties.objects.get(user=question.author)
                usr = request.user
            except Question.DoesNotExist:
                return HttpResponse("None")
            except UserProperties.DoesNotExist:
                return HttpResponse("None")
            try:
                like = question.rating.get(user=usr)  # will throw another exception if Many (not 1) matching results
                if abs(like.state + like_state) <= 1:
                    like.state = like.state+like_state
                    like.save()
                    UserProperties.objects.filter(user=question.author).update(rating=author_account.rating+like_state)
            except Like.DoesNotExist:
                # create new like if no like
                if abs(like_state) == 1:
                    new_like = Like.objects.create(user=usr, state=like_state)
                    question.rating.add(new_like)
                    UserProperties.objects.filter(user=question.author).update(rating=author_account.rating+like_state)
            return HttpResponse(Question.objects.get(id=pid).rating)
    return HttpResponse(None)


@csrf_exempt
@require_POST
def like_answer(request):
    if request.user.is_authenticated():
        form = Like(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            pid = data["id"]
            like_state = data["like"]
            try:
                answer = Answer.objects.get(id=pid)
                author_account = UserProperties.objects.get(user=answer.author)
                usr = request.user
            except Answer.DoesNotExist:
                return HttpResponse("None")
            except UserProperties.DoesNotExist:
                return HttpResponse("None")
            try:
                like = answer.rating.get(user=usr)
                if abs(like.state + like_state) <= 1:
                    like.state = like.state+like_state
                    like.save()
                    UserProperties.objects.filter(user=answer.author).update(rating=author_account.rating+like_state)
            except Like.DoesNotExist:
                if abs(like_state) == 1:
                    new_like = Like.objects.create(user=usr, state=like_state)
                    answer.rating.add(new_like)
                    UserProperties.objects.filter(user=answer.author).update(rating=author_account.rating+like_state)
            return HttpResponse(Answer.objects.get(id=pid).rating)
    return HttpResponse(None)


#
# - add a page dividing results by tag / by question ???
#
@csrf_exempt
@require_POST
def search(request):
    if request.method == "POST":
        input = request.POST["input"]
        # smth here ...

        return HttpResponse({"text": "JSON result ... "}, content_type="application/json")
