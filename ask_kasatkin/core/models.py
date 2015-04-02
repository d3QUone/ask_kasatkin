# coding:utf8
from django.db import models
from django.contrib.auth.models import User
from time import time  # cause timestamps are better :)


# question-class - OK
class Question(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User)
    has_answer = models.BooleanField(default=False)  # when author chooses an answer set 1
    date = models.DateTimeField(auto_now_add=True)   # will use to add date on pages


# answer-class - OK
class Answer(models.Model):
    text = models.TextField()
    rating = models.IntegerField(default=0)
    chosen = models.BooleanField(default=False)  # + only one answer can be marked in one question
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)  # which question to answer
    date = models.DateTimeField(auto_now_add=True)


# used for searching tips & loading tags
class TagName(models.Model):
    name = models.CharField(max_length=100)


# link unique tags with many questions
class StoreTag(models.Model):
    tag = models.ForeignKey(TagName)
    question = models.ForeignKey(Question)



# likes
class LikesQuestions(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    state = models.IntegerField(default=0)  # default - no vote. vars: -1, 0, 1


class LikesAnswers(models.Model):
    user = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)
    state = models.IntegerField(default=0)
