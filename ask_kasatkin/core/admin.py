from django.contrib import admin
from core.models import Question


class question_admin(admin.ModelAdmin):
    fields = ['title', 'rating', 'author']


admin.site.register(Question, question_admin)