from django.contrib import admin
from core.models import the_question


class question_admin(admin.ModelAdmin):
    fields = ['title', 'rating', 'author']


admin.site.register(the_question, question_admin)