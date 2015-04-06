from django import forms


class NewQuestion(forms.Form):
    title = forms.CharField(min_length=10, max_length=100)
    #text = forms.Textarea()  # WTF with that????
    text = forms.CharField(min_length=10)
    tags = forms.CharField(required=False)
    '''
    def clean(self):
        title = self.cleaned_data.get("title", "")
        text = self.cleaned_data.get("text", "")
        if title and len(title) < 10:
            raise forms.ValidationError("Use at least 10 symbols in the title")
        if text and len(text) < 10:
            raise forms.ValidationError("Detail your problem (10 chars min)")
        return self.cleaned_data
    '''


class NewAnswer(forms.Form):
    text = forms.CharField(min_length=15)
    redirect_id = forms.IntegerField(min_value=0, required=True)


class LikeAJAX(forms.Form):
    id = forms.IntegerField(min_value=0)
    like = forms.IntegerField(min_value=-1, max_value=1)
