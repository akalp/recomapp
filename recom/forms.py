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