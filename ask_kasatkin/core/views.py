# coding:utf8

import sys
reload(sys)
sys.setdefaultencoding('utf8') # make UTF 8 global-hack

from core.models import Question, Answer, TagName, Like
from core.forms import LikeAJAX, NewQuestion, NewAnswer
from user_profile.models import UserProperties
from user_profile.views import get_user_data
from common_methods import get_static_data
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie  # reset csrf-checkup, will use in AJAX
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse, Http404, JsonResponse         # jquery simple return
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
import thread
import requests


@ensure_csrf_cookie
def index_page(request):
    try:
        page = int(request.GET.get("page", "1"))
    except ValueError:
        raise Http404

    query = request.GET.get("query", "latest")
    if query != "popular":
        paginator = Paginator(Question.objects.all().order_by('-id').prefetch_related("tags", "author", "answers"), 30)
    else:
        paginator = Paginator(Question.objects.all().order_by('-rating').prefetch_related("tags", "author", "answers"), 30)

    try:
        questions_to_render = paginator.page(page)
    except EmptyPage:
        questions_to_render = paginator.page(paginator.num_pages)

    data = get_static_data()
    data["personal"] = get_user_data(request)  # processes all user's-stuff
    data["page"] = page
    data["query"] = query
    data["paginator"] = questions_to_render
    return render(request, "core__index.html", data)


##### QUESTION THREAD #####

# shows a concrete thread: question + answers, allows logged in users add answers, vote
@ensure_csrf_cookie
def question_thread(request, qid=0, error=None):
    if qid != 0:
        try:
            question = Question.objects.filter(id=qid).select_related("tags", "author", "answers")[0]
        except Question.DoesNotExist:
            raise Http404
        try:
            page = int(request.GET.get("page", "1"))
        except ValueError:
            raise Http404

        data = get_static_data()
        data["personal"] = get_user_data(request)
        data["error"] = error
        data["question"] = question
        if question.author.user == request.user:
            data["owner"] = True
        else:
            data["owner"] = False

        paginator = Paginator(question.answers.all().order_by('-rating').select_related("author"), 30)
        try:
            ans_to_render = paginator.page(page)
        except EmptyPage:
            ans_to_render = paginator.page(paginator.num_pages)
        data["page"] = page
        data["paginator"] = ans_to_render
        return render(request, "core__question_page.html", data)
    else:
        # we can show some prepared hint-pages in such cases e.g. how to register / add question / ...
        return index_page(request)


##### QUESTIONS ######

# GET -> show add-page
# POST -> process input form
def new_question(request):
    data = get_static_data()
    if request.user.is_authenticated():
        data["personal"] = get_user_data(request)  # processes all user's-stuff
        if request.method == "POST":
            form = NewQuestion(request.POST or None)
            if form.is_valid():
                data = form.cleaned_data
                title = data["title"]
                text = data["text"]
                tags = data["tags"].replace(" ", "").split(",")

                quest = Question.objects.create(title=title[:250], text=text, author=UserProperties.objects.get(user=request.user))
                for t in tags[:3]:
                    if len(t) > 0:
                        try:
                            tn = TagName.objects.get(name=str(t).lower())
                        except TagName.DoesNotExist:
                            tn = TagName.objects.create(name=str(t).lower())
                        quest.tags.add(tn)
                return question_thread(request, qid=quest.id)
            else:
                data["form"] = form
    return render(request, "core__ask.html", data)


# send update to notification server in new thread
def push_updates(update):
    requests.post("http://vksmm.info:8888/push", data=update)


# adding-answer method
def add_new_answer(request):
    error = None
    if request.user.is_authenticated():
        form = NewAnswer(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            redirect_id = data["redirect_id"]
            redirect_page = data["redirect_page"]
            text = data["text"]

            author = UserProperties.objects.get(user=request.user)
            new_answer = Answer.objects.create(text=text, author=author)
            question = Question.objects.filter(id=redirect_id).select_related("author")[0]
            question.answers.add(new_answer)

            # send main in new thread
            thread.start_new_thread(send_mail, (
                "New answer to {0}".format(question.title),
                """Check new answer from user "{0}" to your question "{1}" by this URL: vksmm.info{2}""".format(
                    UserProperties.objects.get(user=request.user).nickname,
                    question.title,
                    reverse("core:question", kwargs={"qid": redirect_id}) + "?page={0}#answer_{1}".format(redirect_page, new_answer.id)
                ),
                "ask_kasatkin@mail.ru",
                [question.author.user.email]
            ))

            # send notification in new thread
            thread.start_new_thread(push_updates, ({
                "channel": question.id,
                "id": new_answer.id,
                "text": new_answer.text,
                "avatar": author.filename,
                "nickname": author.nickname
            },))

            return redirect(reverse("core:question", kwargs={"qid": redirect_id}) + "?page={0}#answer_{1}".format(redirect_page, new_answer.id))
        else:
            redirect_id = request.POST["redirect_id"]
            error = form
            return question_thread(request, qid=redirect_id, error=error)


##### TAGS ######

@ensure_csrf_cookie
@require_GET
def all_by_tag(request, tag_n=None):
    data = get_static_data()
    if tag_n:
        data["tag"] = tag_n.lower()
        try:
            page = int(request.GET.get("page", "1"))
        except ValueError:
            raise Http404
        try:
            #paginator = Paginator(Question.objects.filter(tags=TagName.objects.get(name=tag_n.lower())).select_related("tags", "author", "answers"), 30)  # 27 hits total
            paginator = Paginator(TagName.objects.get(name=tag_n.lower()).question_set.all().select_related("tags", "author", "answers"), 30)  # 27 hits total too..
            try:
                q_to_render = paginator.page(page)
            except EmptyPage:
                q_to_render = paginator.page(paginator.num_pages)  # TODO: find paginator error names
            data["page"] = page
            data["paginator"] = q_to_render
        except TagName.DoesNotExist:
            data["paginator"] = None
    else:
        raise Http404
    data["personal"] = get_user_data(request)  # processes all user's-stuff
    return render(request, "core__by_tag.html", data)


##### USER PROFILE (additional feature) #####

# - separate page for Stats
# - separate page for question-preview, answer-preview
@require_GET
def user_profile_stats(request, id=None):
    data = get_static_data()
    if id:
        try:
            current_user = UserProperties.objects.get(user=User.objects.get(id=id))
        except UserProperties.DoesNotExist:
            raise Http404
        data["profile"] = current_user
        data["total_questions"] = Question.objects.filter(author=current_user).count()
        data["total_answers"] = Answer.objects.filter(author=current_user).count()
    else:
        data["error"] = "No profile selected :("
    data["personal"] = get_user_data(request)
    return render(request, "core__user_stats.html", data)


@require_GET
def user_profile_all_data(request):

    # paginator for all questions / or separate page with all questions and all answers
    return None


##### jQuery-AJAX (POST) methods #####

@require_POST
def like_post(request):
    if request.user.is_authenticated():
        form = LikeAJAX(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            pid = data["id"]
            like_state = data["like"]
            try:
                question = Question.objects.filter(id=pid).select_related("author", "rating")[0]
                author_account = question.author
                usr = UserProperties.objects.get(user=request.user)
            except Question.DoesNotExist:
                return HttpResponse("None")
            except UserProperties.DoesNotExist:
                return HttpResponse("None")
            try:
                like = question.likes.get(user=usr)  # will throw another exception if Many (not 1) matching results
                if abs(like.state + like_state) <= 1:
                    like.state += like_state
                    like.save()
                    Question.objects.filter(id=pid).update(rating=question.rating+like_state)
                    UserProperties.objects.filter(id=author_account.id).update(rating=author_account.rating+like_state)
            except Like.DoesNotExist:
                # create new like if no like from this used
                if abs(like_state) == 1:
                    new_like = Like.objects.create(user=usr, state=like_state)
                    question.likes.add(new_like)
                    Question.objects.filter(id=pid).update(rating=question.rating+like_state)
                    UserProperties.objects.filter(id=author_account.id).update(rating=author_account.rating+like_state)
            return HttpResponse(Question.objects.get(id=pid).rating)
    return HttpResponse("None")


@require_POST
def like_answer(request):
    if request.user.is_authenticated():
        form = LikeAJAX(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            pid = data["id"]
            like_state = data["like"]
            try:
                answer = Answer.objects.filter(id=pid).select_related("author", "rating")[0]
                author_account = answer.author
                usr = UserProperties.objects.get(user=request.user)
            except Answer.DoesNotExist:
                return HttpResponse("None")
            except UserProperties.DoesNotExist:
                return HttpResponse("None")
            try:
                like = answer.likes.get(user=usr)
                if abs(like.state + like_state) <= 1:
                    like.state += like_state
                    like.save()
                    Answer.objects.filter(id=pid).update(rating=answer.rating+like_state)
                    UserProperties.objects.filter(id=author_account.id).update(rating=author_account.rating+like_state)
            except Like.DoesNotExist:
                if abs(like_state) == 1:
                    new_like = Like.objects.create(user=usr, state=like_state)
                    answer.likes.add(new_like)
                    Answer.objects.filter(id=pid).update(rating=answer.rating+like_state)
                    UserProperties.objects.filter(id=author_account.id).update(rating=author_account.rating+like_state)
            return HttpResponse(Answer.objects.get(id=pid).rating)
    return HttpResponse("None")


@require_POST
def mark_as_true(request):
    if request.user.is_authenticated():
        try:
            answer_id = int(request.POST.get("id"))
        except ValueError:
            return HttpResponse("None")
        try:
            a = Answer.objects.get(id=answer_id)
            q = Question.objects.filter(answers=a).select_related("author")[0]
            if q.author != UserProperties.objects.get(user=request.user):
                return HttpResponse("None")

            if not q.has_answer:
                # has not answer -> add answer
                a.chosen = True
                a.save()  #Answer.objects.filter(id=answer_id).update(chosen=True)
                q.has_answer = True
                q.save()
                return HttpResponse("True")
            else:
                if a.chosen:
                    a.chosen = False
                    a.save()
                    q.has_answer = False
                    q.save()
                    return HttpResponse("False")
        except Answer.DoesNotExist, Question.DoesNotExist:
            return HttpResponse("None")
    return HttpResponse("None")


#
# - add a page dividing results by tag / by question ???
#
@csrf_exempt
@require_POST
def search(request):
    if request.method == "POST":
        input = request.POST.get("input", "")

        # our search business here ...

        return HttpResponse({"text": "JSON result ... "}, content_type="application/json")
