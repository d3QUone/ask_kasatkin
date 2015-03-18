# coding:utf8
from django.db import models
from django.contrib.auth.models import User
from time import time  # cause timestamps are better :)


# additional user properties - OK
class user_properties(models.Model):
    user = models.ForeignKey(User)
    nickname = models.CharField(max_length=100)  # 2 unique fields
    rating = models.IntegerField(default=0)
    filename = models.CharField(max_length=100)  # avatar filename!


# question-class - OK
class the_question(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User)

    # any need in this??? (i though to mark question on main page)
    the_answer_was_chosen = models.IntegerField(default=0)  # when author chooses an answer set 1

    date = models.BigIntegerField(default=0)
    def save(self, *args, **kwargs):
        if not self.id:
            self.date = int(time())
        return super(the_question, self).save(*args, **kwargs)


# answer-class - OK
class the_answer(models.Model):
    text = models.TextField()
    rating = models.IntegerField(default=0)
    is_marked_as_true = models.BooleanField(default=False)  # + only one answer can be marked in one question
    author = models.ForeignKey(User)
    contributed_to = models.ForeignKey(the_question)  # which question to answer

    date = models.BigIntegerField(default=0)
    def save(self, *args, **kwargs):
        if not self.id:
            self.date = int(time())
        return super(the_answer, self).save(*args, **kwargs)


# used for searching tips & loading tags
class tag_name(models.Model):
    name = models.CharField(max_length=100)


# link unique tags with many questions
class store_tag(models.Model):
    tag = models.ForeignKey(tag_name)
    question = models.ForeignKey(the_question)


'''
# don't create this tables while I'm not using them

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
'''