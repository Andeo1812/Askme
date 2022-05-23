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
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-group mb-3"}), label="Name", max_length=64)
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-group mb-3"}), label="Surname", required=False, max_length=64)
    avatar = forms.FileField(widget=forms.FileInput(attrs={"class": "form-group mb-3"}), label="Avatar", required=False, max_length=64)

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
#
# class SettingsForm(forms.ModelForm):
#     avatar = forms.FileField(widget=forms.FileInput(attrs={"class": "form-group mb-3"}), label="Аватар", required=False)
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'avatar', ]
#         labels = {
#             "username": "Логин",
#             "first_name": "Ник",
#         }
#         widgets = {
#             "username": forms.TextInput(attrs={"class": "form-group mb-3", "readonly": "readonly"}),
#             "first_name": forms.TextInput(attrs={"class": "form-group mb-3"})
#         }
#         help_texts = {
#             'username': None,
#         }
#
#     def save(self, *args, **kwargs):
#         user = super().save(*args, *kwargs)
#         user.profile_related.avatar = self.cleaned_data['avatar']
#         user.profile_related.save()
#         return user


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


# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer
#         fields = ('text',)
#         widgets = {
#             "text": forms.Textarea(attrs={"class": "form-group mb-3", "placeholder": "Введите ваш ответ"})
#         }
