# coding:utf8
from django.db import models
from django.contrib.auth.models import User

import datetime

class user_properties(models.Model):
    user = models.ForeignKey(User)
    nickname = models.CharField(max_length=100)  # 2 unique fields
    rating = models.IntegerField(default=0)


class the_question(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    the_answer_was_chosen = models.IntegerField(default=0) # when author chooses an answer set 1
    author = models.ForeignKey(User)

    date = models.DateTimeField(editable=False)
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date = datetime.datetime.today()
        return super(the_question, self).save(*args, **kwargs)


class the_answer(models.Model):
    text = models.TextField()
    rating = models.IntegerField(default=0)
    is_marked_as_true = models.BooleanField(default=False) # + only one answer can be marked in one question
    author = models.ForeignKey(User)
    contributed_to = models.ForeignKey(the_question) # which question to answer

    date = models.DateTimeField(editable=False)
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.date = datetime.datetime.today()
        return super(the_answer, self).save(*args, **kwargs)


class the_tag(models.Model):
    name = models.CharField(max_length=100)
    used_in = models.ForeignKey(the_question)


#       add class to store
#      votes of the members
#       /               \
# to questions      to answers
