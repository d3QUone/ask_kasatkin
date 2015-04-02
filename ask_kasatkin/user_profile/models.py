from django.db import models
from django.contrib.auth.models import User


# additional user properties - OK
class UserProperties(models.Model):
    user = models.ForeignKey(User)
    nickname = models.CharField(max_length=20)
    rating = models.IntegerField(default=0)
    avatar = models.ImageField()  # isn't used yet
    filename = models.CharField(max_length=100)  # delete this soon...
