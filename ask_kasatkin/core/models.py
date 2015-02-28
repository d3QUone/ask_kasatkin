from django.db import models


# the user :)
class the_user(models.Model):
    email = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    avatar_link = models.CharField(max_length=200) # link to static file on the f-server ?
    date = models.DateTimeField("user was registered")
    rating = models.IntegerField(default=0)


class the_tag(models.Model):
    name = models.CharField(max_length=100)
    # to show the most popular tag -- increased when tag was added
    used_times = models.IntegerField(default=1)


class the_question(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    date = models.DateTimeField("question date")
    rating = models.IntegerField(default=0)

    author = models.ForeignKey(the_user)
    tags = models.ForeignKey(the_tag)

    # when author chooses an answer set this 1
    the_answer_was_chosen = models.IntegerField(default=0)


class the_answer(models.Model):
    text = models.TextField()
    date = models.DateTimeField("answer date")
    rating = models.IntegerField(default=0)
    # + only one answer can be marked in one question
    is_marked_as_true = models.BooleanField(default=False)

    author = models.ForeignKey(the_user)
    contributed_to = models.ForeignKey(the_question) # which question to answer