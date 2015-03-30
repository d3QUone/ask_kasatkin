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
from user_profile.models import user_properties
from core.models import the_question, the_answer, tag_name, store_tag

from datetime import datetime
from time import time
from uuid import uuid4
from random import randint


# create some users automatically
def create():
    timestamp = int(time())
    username = "test_{0}".format(uuid4())[:30]  # django max size
    email = "{0}@test.com".format(timestamp)
    password = "forever1"  # not to forget :)

    new_user = User.objects.create_user(username=username, email=email, password=password)
    new_user.save()

    user_properties.objects.create(
        user=new_user,
        filename="ex1",
        nickname=username,
    )
    return new_user


# just returns a test user from DB
def select_random_user():
    random_user = User.objects.all().filter(username__startswith="test")
    if random_user:
        user = random_user[randint(1, len(random_user)) - 1]
        return user
    else:
        return None


def create_random_question(amount):
    test_set = "{0}-test".format(datetime.now())
    for i in range(amount):
        user = select_random_user()
        if not user:
            user = create()

        # create question
        question = the_question.objects.create(
            author=user,
            title=test_set,
            text="Test question\n" + "\n".join([str(uuid4())*2 for i in range(11)]),
        )

        # add tags to question
        try:
            tn = tag_name.objects.get(name="test_set_{0}".format(i))
        except:
            tn = tag_name.objects.create(name="test_set_{0}".format(i))

        new_tag = store_tag()
        new_tag.question = question
        new_tag.tag = tn
        new_tag.save()

        # create answer
        how_much = int(randint(0, 6))
        create_random_answers(question.id, how_much)


def create_random_answers(question_id=None, amount=0):
    if question_id:
        ques = the_question.objects.get(id=question_id)
        for i in range(amount):
            user = select_random_user()
            if not user:
                user = create()

            the_answer.objects.create(
                text="Test answer\n" + "\n".join(["{0}) {1}".format(i, uuid4()) for i in range(5)]),
                author=user,
                contributed_to=ques
            )


def fb():
    t0 = datetime.now()
    for i in range(100):
        create()
    create_random_question(100)
    print "Done in {0}".format(datetime.now() - t0)


fb()
