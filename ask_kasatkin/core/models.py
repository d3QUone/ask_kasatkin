# coding:utf8
from django.db import models
from user_profile.models import UserProperties


class Like(models.Model):
    user = models.ForeignKey(UserProperties)
    state = models.IntegerField(default=0)


# answer-class - OK
class Answer(models.Model):
    text = models.TextField()
    chosen = models.BooleanField(default=False)  # + only one answer can be marked in one question
    author = models.ForeignKey(UserProperties)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Like)
    rating = models.IntegerField(default=0)


# used for searching tips & loading tags
class TagName(models.Model):
    name = models.CharField(max_length=100)


# question-class - OK
class Question(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    author = models.ForeignKey(UserProperties)       # right dependency
    has_answer = models.BooleanField(default=False)  # when author chooses an answer set 1
    date = models.DateTimeField(auto_now_add=True)   # will use to add date on pages
    answers = models.ManyToManyField(Answer)
    tags = models.ManyToManyField(TagName)
    likes = models.ManyToManyField(Like)
    rating = models.IntegerField(default=0)


'''
# some model-tests

from core.models import Like, Question, Answer, TagName

u = User.objects.create_user(username="volkvid", email="volkvid@yandex.ru", password="qwerty")
UserProperties.objects.create(user=u, nickname="Vladimir", avatar="ex2", filename="ex3")
q1 = Question.objects.create(title="testing many2many", text="returning val by 'get' if it surely has 1 answer :)", author=u)
l = Like.objects.create(state=1, user=u)
q1.likes.add(l)
q1.rating += l.state
q1.save()

a1 = Answer.objects.create(text="answezxczk owieom xa \n adsid u1", author=u)
q1.answers.add(a1)
ans = q1.answers.get(author=u)
'''
