# coding:utf8
from django.db import models
from django.contrib.auth.models import User

import time  # cause timestamps are better :)

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

    date = models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        if not self.id:
            self.date = int(time.time())
        return super(the_question, self).save(*args, **kwargs)


class the_answer(models.Model):
    text = models.TextField()
    rating = models.IntegerField(default=0)
    is_marked_as_true = models.BooleanField(default=False) # + only one answer can be marked in one question
    author = models.ForeignKey(User)
    contributed_to = models.ForeignKey(the_question) # which question to answer

    date = models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        if not self.id:
            self.date = int(time.time())
        return super(the_answer, self).save(*args, **kwargs)


# used for searching tips
class the_tag(models.Model):
    name = models.CharField(max_length=100)


# USE MANY TO MANY for linking unique tags with questions
class store_tag(models.Model):
    tag = models.ForeignKey(the_tag)
    question = models.ForeignKey(the_question)
    name = models.CharField(max_length=100) # name -> the_tag???


# save for Questions
class likes_questions(models.Model):
    user_id = models.ForeignKey(User)
    question_id = models.ForeignKey(the_question)
    state = 0  # default - no vote. vars: -1, 0, 1


# save for Answers
class likes_answers(models.Model):
    user_id = models.ForeignKey(User)
    answer_id = models.ForeignKey(the_answer)
    state = 0

# render likes:
#