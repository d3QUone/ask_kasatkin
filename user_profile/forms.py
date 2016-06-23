from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(min_length=5, max_length=30)
    password = forms.CharField(min_length=5)


class RegistrationForm(forms.Form):
    input_login = forms.CharField(min_length=5, max_length=30)      # check if no doubles
    input_nickname = forms.CharField(min_length=5, max_length=20)
    input_email = forms.EmailField(min_length=5)
    input_password = forms.CharField(min_length=5)
    input_password_rep = forms.CharField(min_length=5)
    avatar = forms.ImageField(required=True)

    def clean(self):
        pas1 = self.cleaned_data.get("input_password")
        pas2 = self.cleaned_data.get("input_password_rep")
        if pas1 and pas1 != pas2:
            raise forms.ValidationError("Passwords are not equal")
        return self.cleaned_data
