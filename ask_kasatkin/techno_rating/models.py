from django.db import models

# techno-start idea
class TechIdea(models.Model):
	tech_id = models.IntegerField(default=0)
	name = models.CharField(max_length=300)
	like = models.IntegerField(default=0)
	comm = models.IntegerField(default=0)
