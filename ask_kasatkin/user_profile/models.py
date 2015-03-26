from django.db import models
from django.contrib.auth.models import User


# additional user properties - OK
class user_properties(models.Model):
    user = models.ForeignKey(User)
    nickname = models.CharField(max_length=100)  # 2 unique fields
    rating = models.IntegerField(default=0)
    filename = models.CharField(max_length=100)  # avatar filename!