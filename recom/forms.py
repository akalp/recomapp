from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User, Movie, Book, Music, MusicGenre, MovieGenre, BookGenre, \
    Album, Author, Director, Performer, Singer

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
        fields = ('first_name', 'last_name', 'birthday', 'info', 'profile_photo')


        widgets = {
            'birthday': forms.SelectDateWidget(years=range(1919, datetime.now().year + 1)),
        }

        help_texts = {
            'info': 'Max 250 characters.'
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


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'
        exclude = ('wished_by',)

        widgets = {
            'publish_date': forms.SelectDateWidget(years=range(1919, datetime.now().year + 1)),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ('wished_by',)

        widgets = {
            'publish_date': forms.SelectDateWidget(years=range(1919, datetime.now().year + 1)),
        }


class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = '__all__'
        exclude = ('wished_by',)

        widgets = {
            'publish_date': forms.SelectDateWidget(years=range(1919, datetime.now().year + 1)),
        }


class MovieGenreForm(forms.ModelForm):
    class Meta:
        model = MovieGenre
        fields = '__all__'


class BookGenreForm(forms.ModelForm):
    class Meta:
        model = BookGenre
        fields = '__all__'


class MusicGenreForm(forms.ModelForm):
    class Meta:
        model = MusicGenre
        fields = '__all__'


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = '__all__'


class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = '__all__'


class PerformerForm(forms.ModelForm):
    class Meta:
        model = Performer
        fields = '__all__'


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class SingerForm(forms.ModelForm):
    class Meta:
        model = Singer
        fields = '__all__'