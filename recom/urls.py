"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from recom import views

from recom.views import IndexView, MovieIndex, MovieDetailView, MovieBestListView, MovieTrendListView, BookIndex, \
    BookBestListView, BookTrendListView, BookDetailView, MusicIndex, MusicBestListView, MusicTrendListView, MusicDetailView

app_name = 'recom'

urlpatterns = [
    path('', IndexView.as_view()),
    path('movies', MovieIndex.as_view(), name="movie_list"),
    path('movies/best', MovieBestListView.as_view(), name="movie_best"),
    path('movies/trends', MovieTrendListView.as_view(), name="movie_trend"),
    path('movies/<pk>', MovieDetailView.as_view(), name="movie_detail"),
    path('books', BookIndex.as_view(), name="book_list"),
    path('books/best', BookBestListView.as_view(), name="book_best"),
    path('books/trends', BookTrendListView.as_view(), name="book_trend"),
    path('books/<pk>', BookDetailView.as_view(), name="book_detail"),
    path('music', MusicIndex.as_view(), name="music_list"),
    path('music/best', MusicBestListView.as_view(), name="music_best"),
    path('music/trends', MusicTrendListView.as_view(), name="music_trend"),
    path('music/<pk>', MusicDetailView.as_view(), name="music_detail")
]
