from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User

from datetime import datetime


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'birthday', 'profile_photo')

        widgets = {
            'birthday': forms.SelectDateWidget(years=range(1919, datetime.now().year+1))
        }


class UserEditForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'birthday', 'profile_photo')


        widgets = {
            'birthday': forms.SelectDateWidget(years=range(1919, datetime.now().year + 1)),
        }

    def clean(self):
        cleaned = dict()
        for key, value in self.cleaned_data.items():
            if value != "":
                cleaned[key] = value
        return cleaned


    def save(self, commit=True):
        print(self.cleaned_data)
        print(self.changed_data)

        user = super().save()
        if "password" in self.cleaned_data.keys():
            user.set_password(self.cleaned_data.get("password"))
            user.save()

        return user
