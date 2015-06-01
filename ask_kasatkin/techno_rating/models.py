from django.db import models


# techno-start idea
class TechIdea(models.Model):
	name = models.CharField(max_length=300)
	link = models.CharField(max_length=300)  # full url
	like = models.IntegerField(default=0)
	comm = models.IntegerField(default=0)
		