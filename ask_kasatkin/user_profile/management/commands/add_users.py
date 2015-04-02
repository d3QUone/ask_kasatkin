from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User
from user_profile.models import UserProperties

from time import time
from uuid import uuid4


'''
Requirements:

Users > 10 000
Questions > 100 000
Answers > 1 000 000
Tags > 10 000
Likes > 2 000 000
'''


class Command(NoArgsCommand):
    def create(self):
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