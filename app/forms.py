from django import forms
from django.core.validators import ValidationError

from app.models import *


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-group mb-3"}), label="Login", max_length=64)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-group mb-3"}), label='Password', max_length=64)

    def clean_password(self):
        data = self.cleaned_data['password']
        if len(data) < 9:
            raise ValidationError("Password should be more then 8 symbols.")
        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        if len(data) < 9:
            raise ValidationError("Username should be more then 8 symbols.")
        return data


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-group mb-3"}), label="login", max_length=48)
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-group mb-3"}), label="Email", max_length=64)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-group mb-3"}), label='Password', max_length=64)
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-group mb-3"}), label='Repeat password', max_length=64)

    def clean_password(self):
        data = self.data['password']
        if len(data) < 9:
            raise ValidationError("Password should be more then 8 symbols.")
        return data

    def clean_username(self):
        data = self.data['username']
        if len(data) < 9:
            raise ValidationError("Username should be more then 8 symbols.")
        return data

    def clean_password_repeat(self):
        passwd_one = self.data['password']
        passwd_two = self.data['password_repeat']
        if passwd_one != passwd_two:
            raise ValidationError("Passwords do not match")


class AskForm(forms.ModelForm):
    tag_list = forms.CharField(widget=forms.TextInput(attrs={"class": "form-group mb-3",
                                                             "placeholder": "Specify one or more tags"}),
                               label="Tags")

    class Meta:
        model = Question
        fields = ("title", "text",)
        labels = {
            "title": "Header",
            "text": "Question wording",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-group mb-3", "placeholder": "Question wording"}),
            "text": forms.Textarea(attrs={"class": "form-group mb-3", "placeholder": "Peculiarities of C++ multithreading?"})
        }

    def clean_tag_list(self):
        data = self.data['tag_list']
        if len(data) > 63:
            raise ValidationError("Tags should be less then 64 symbols.")
        return data

    def clean_title(self):
        data = self.data['title']
        if len(data) > 127:
            raise ValidationError("Title should be less then 128 symbols.")
        return data

    def clean_text(self):
        data = self.data['text']
        if len(data) > 2027:
            raise ValidationError("Description should be less then 2028 symbols.")
        return data


class AnswerForm(forms.ModelForm):
    tag_list = forms.CharField(widget=forms.TextInput(attrs={"class": "form-group mb-3",
                                                             "placeholder": "Specify one or more tags"}),
                               label="Tags")

    class Meta:
        model = Answer
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-group mb-3", "placeholder": "Input your answer"})
        }

    def clean_text(self):
        data = self.data['text']
        if len(data) > 2027:
            raise ValidationError("Description should be less then 2028 symbols.")
        return data


class SettingsForm(forms.ModelForm):
    avatar = forms.FileField(widget=forms.FileInput(attrs={"class": "form-group mb-3"}), label="Avatar", required=False)
    username = forms.CharField(disabled=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-group mb-3"}), label="Email", max_length=64)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'avatar', ]
        labels = {
            "username": "Login",
            "first_name": "Name",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-group mb-3", "readonly": "readonly"}),
            "first_name": forms.TextInput(attrs={"class": "form-group mb-3"})
        }
        help_texts = {
            'username': None,
        }

    def save(self, *args, **kwargs):
        user = super().save(*args, *kwargs)
        if (self.cleaned_data['avatar']):
            user.profile_related.avatar = self.cleaned_data['avatar']
            user.profile_related.save()
        return user
