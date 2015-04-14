from django.db import models
from django.contrib.auth.models import User

# can use OneToOneField for unique objects

# additional user properties - OK
class UserProperties(models.Model):
    user = models.ForeignKey(User) #OneToOne
    nickname = models.CharField(max_length=20)
    rating = models.IntegerField(default=0)
    filename = models.CharField(max_length=100)
