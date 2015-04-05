#
# some automatic for testing
#
# Usage:
# >> python fill_base.py
#

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ask_kasatkin.settings")
django.setup()

# now we are able to fetch django methods

from django.contrib.auth.models import User
from user_profile.models import UserProperties
from core.models import Question, Answer, TagName, StoreTag, LikesQuestions, LikesAnswers

from datetime import datetime
from time import time
from uuid import uuid4
from random import randint


# create one user
def create_user():
    timestamp = int(time())
    username = "test_{0}".format(uuid4())[:30]  # django max size
    email = "{0}@test.com".format(timestamp)
    password = "forever1"  # not to forget :)

    new_user = User.objects.create_user(username=username, email=email, password=password)
    new_user.save()

    UserProperties.objects.create(
        user=new_user,
        filename="ex1",
        nickname=username[:20],
    )
    return new_user


# 1 user -> 10 questions -> 100 answers -> 1 tag -> 200 likes

def create_question(user):
    # add 1 tag
    tag_name = "test_set_{0}".format(user.login)
    try:
        tn = TagName.objects.get(name=tag_name)
    except:
        tn = TagName.objects.create(name=tag_name)

    # 10 question on 1 user
    for i in range(10):
        test_set = "{0}-test".format(datetime.now())

        # create question
        question = Question.objects.create(
            author=user,
            title=test_set,
            text="Test question\n" + "\n".join([str(uuid4())*2 for i in range(8)]),
        )
        # link the tag
        StoreTag.objects.create(question=question, tag=tn)

        for j in range(10):
            Answer.objects.create(
                text="Test answer\n" + "\n".join(["{0}) {1}".format(i, uuid4()) for i in range(4)]),
                author=user,
                contributed_to=question
            )


# + add likes..., but at the end
def do_likes():
    question_amount = Question.objects.all().count()
    answer_amount = Answer.objects.filter("-id").count()

    for user in User.objects.all():
        print user.id
        for i in range(100):
            # 100 on random questions
            question = Question.objects.get(id=randint(0, question_amount))
            LikesQuestions.objects.create(question=question, user=user, state=1)
            owner = UserProperties.objects.get(user=question.author)
            UserProperties.objects.filter(user=question.author).update(rating=owner.rating + 1)

            # and 100 on random answers by every user
            answer = Answer.objects.get(id=randint(0, answer_amount))
            LikesAnswers.objects.create(answer=answer, user=user, state=1)
            owner = UserProperties.objects.get(user=answer.author)
            UserProperties.objects.filter(user=answer.author).update(rating=owner.rating + 1)


def fb():
    t0 = datetime.now()
    total_users = User.objects.all().count()
    print "{0} users now".format(total_users)
    for i in range(10000 - total_users):
        user = create_user()
        create_question(user=user)
    do_likes()
    print "Done in {0}".format(datetime.now() - t0)


fb()


'''
Requirements:

Users > 10 000
Questions > 100 000
Answers > 1 000 000
Tags > 10 000
Likes > 2 000 000
'''
