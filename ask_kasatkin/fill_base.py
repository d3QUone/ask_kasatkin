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
from core.models import Question, Answer, TagName, StoreTag

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
        nickname=username,
    )
    return new_user


def create_question(user):
    # 10 question on 1 user
    for i in range(10):
        test_set = "{0}-test".format(datetime.now())
        tag_name = "test_set_{0}".format(i)

        # create question
        question = Question.objects.create(
            author=user,
            title=test_set,
            text="Test question\n" + "\n".join([str(uuid4())*2 for i in range(11)]),
        )

        # add tags to question
        try:
            tn = TagName.objects.get(name=tag_name)
        except :
            tn = TagName.objects.create(name=tag_name)

        StoreTag.objects.create(question=question, tag=tn)

        # create answer
        how_much = int(randint(0, 6))
        create_random_answers(question.id, how_much)



def create_random_answers(question_id, amount=0):

    if question_id:
        ques = Question.objects.get(id=question_id)
        for i in range(amount):

            Answer.objects.create(
                text="Test answer\n" + "\n".join(["{0}) {1}".format(i, uuid4()) for i in range(5)]),
                author=user,
                contributed_to=ques
            )


def fb():
    t0 = datetime.now()
    total_users = User.objects.all().count()
    print "{0} users now".format(total_users)
    for i in range(10000 - total_users):
        create_user()

    # we have 10000 users now...
    total_questions = Question.objects.all().count()
    for user in User.objects.all():
        create_question(user=user)


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
