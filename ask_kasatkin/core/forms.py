from django import forms
from core.models import Question, Answer, TagName, StoreTag


class NewQuestion(forms.Form):
    title = forms.CharField(min_length=10, max_length=100)
    text = forms.Textarea()
    tags = forms.CharField()


class NewAnswer(forms.Form):
    text = forms.Textarea()


class Like(forms.Form):
    item_id = forms.IntegerField(min_value=0)
    like = forms.IntegerField(min_value=-1, max_value=1)
