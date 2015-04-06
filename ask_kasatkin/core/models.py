# coding:utf8
from django.db import models
from django.contrib.auth.models import User


### what if I have ONE like-table for all fields????
# id-fields will not cross cause "LIKES" will not have any info about owners
# all ids will be in question/answer :)

class Like(models.Model):
    user = models.ForeignKey(User)
    state = models.IntegerField(default=0)


# answer-class - OK
class Answer(models.Model):
    text = models.TextField()
    chosen = models.BooleanField(default=False)  # + only one answer can be marked in one question
    author = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.ManyToManyField(Like)


# used for searching tips & loading tags
class TagName(models.Model):
    name = models.CharField(max_length=100)


# question-class - OK
class Question(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    author = models.ForeignKey(User)
    has_answer = models.BooleanField(default=False)  # when author chooses an answer set 1
    date = models.DateTimeField(auto_now_add=True)   # will use to add date on pages
    # new ideas:
    answers = models.ManyToManyField(Answer)
    tags = models.ManyToManyField(TagName)
    rating = models.ManyToManyField(Like)
