from django import forms

class SigninForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    nextpage = forms.CharField(widget=forms.HiddenInput, required=False)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    def validate_password(self):
        pass

    def validate_username(self):
        pass

    def validate_email(self):
        pass


class ProjectForm(forms.Form):
    project_name = forms.CharField(max_length=100)
