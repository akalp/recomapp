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

urlpatterns = [
    path('login_register/', views.login_register, name='login_register'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.IndexView.as_view(), name="index"),

    path('movies', views.MovieIndex.as_view(), name="movie_index"),
    path('movies/all', views.MovieListView.as_view(), name="movie_list"),
    path('movies/best', views.MovieBestListView.as_view(), name="movie_best"),
    path('movies/trends', views.MovieTrendListView.as_view(), name="movie_trend"),
    path('movies/<pk>', views.MovieDetailView.as_view(), name="movie_detail"),

    path('books/all', views.BookListView.as_view(), name="book_list"),
    path('books', views.BookIndex.as_view(), name="book_index"),
    path('books/best', views.BookBestListView.as_view(), name="book_best"),
    path('books/trends', views.BookTrendListView.as_view(), name="book_trend"),
    path('books/<pk>', views.BookDetailView.as_view(), name="book_detail"),

    path('music', views.MusicIndex.as_view(), name="music_index"),
    path('music/all', views.MusicListView.as_view(), name="music_list"),
    path('music/best', views.MusicBestListView.as_view(), name="music_best"),
    path('music/trends', views.MusicTrendListView.as_view(), name="music_trend"),
    path('music/<pk>', views.MusicDetailView.as_view(), name="music_detail"),

    path('user/<pk>', views.UserDetailView.as_view(), name="user_detail"),
    path('user/<pk>/edit', views.UserEditView.as_view(), name="user_edit"),

    path('wish/<pk>', views.wish, name="wish"),
    path('unwish/<pk>', views.del_wish, name="del_wish"),

    path('follow/<pk>', views.follow_user, name="follow"),
    path('unfollow/<pk>', views.unfollow_user, name="unfollow"),

    path('give_point/', views.give_point, name="give_point"),
    path('get_avg_point/<pk>', views.get_avg_point, name="get_avg"),

    path('make_comment/', views.make_comment, name="make_comment"),
    path('del_comment/<pk>', views.del_comment, name="del_comment"),
    path('like_comment/<pk>', views.like_comment, name="like_comment"),
    path('unlike_comment/<pk>', views.unlike_comment, name="unlike_comment"),

    path('dashboard/', views.Dashboard.as_view(), name="dashboard"),

    path('wishes/<user_pk>', views.WishesListView.as_view(), name="wishes"),
    path('wished/<piece_pk>', views.WishedByListView.as_view(), name="wished_by"),

    path('follows/<user_pk>', views.FollowsListView.as_view(), name="follows"),
    path('followers/<user_pk>', views.FollowerListView.as_view(), name="followers"),

    path('search/', views.SearchListView.as_view(), name="search"),

    path('report/', views.ReportView.as_view(), name="report"),

    path('create_book/', views.BookCreateView.as_view(), name="create_book"),
    path('create_movie/', views.MovieCreateView.as_view(), name="create_movie"),
    path('create_music/', views.MusicCreateView.as_view(), name="create_music"),
    path('create_book_genre/', views.BookGenreCreateView.as_view(), name="create_book_genre"),
    path('create_movie_genre/', views.MovieGenreCreateView.as_view(), name="create_movie_genre"),
    path('create_music_genre/', views.MusicGenreCreateView.as_view(), name="create_music_genre"),
    path('create_album/', views.AlbumCreateView.as_view(), name="create_album"),
    path('create_singer/', views.SingerCreateView.as_view(), name="create_singer"),
    path('create_author/', views.AuthorCreateView.as_view(), name="create_author"),
    path('create_performer/', views.PerformerCreateView.as_view(), name="create_performer"),
    path('create_director/', views.DirectorCreateView.as_view(), name="create_director"),

    path('staff/', views.StaffView.as_view(), name="staff"),
    path('update_book/<pk>', views.BookUpdateView.as_view(), name="update_book"),
    path('update_movie/<pk>', views.MovieUpdateView.as_view(), name="update_movie"),
    path('update_music/<pk>', views.MusicUpdateView.as_view(), name="update_music"),
    path('update_book_genre/<pk>', views.BookGenreUpdateView.as_view(), name="update_book_genre"),
    path('update_movie_genre/<pk>', views.MovieGenreUpdateView.as_view(), name="update_movie_genre"),
    path('update_music_genre/<pk>', views.MusicGenreUpdateView.as_view(), name="update_music_genre"),
    path('update_album/<pk>', views.AlbumUpdateView.as_view(), name="update_album"),
    path('update_singer/<pk>', views.SingerUpdateView.as_view(), name="update_singer"),
    path('update_author/<pk>', views.AuthorUpdateView.as_view(), name="update_author"),
    path('update_performer/<pk>', views.PerformerUpdateView.as_view(), name="update_performer"),
    path('update_director/<pk>', views.DirectorUpdateView.as_view(), name="update_director"),

    path('delete_movie/<pk>', views.MovieDeleteView.as_view(), name="delete_movie"),
    path('delete_book/<pk>', views.BookDeleteView.as_view(), name="delete_book"),
    path('delete_music/<pk>', views.MusicDeleteView.as_view(), name="delete_music"),
    path('delete_movie_genre/<pk>', views.MovieGenreDeleteView.as_view(), name="delete_movie_genre"),
    path('delete_book_genre/<pk>', views.BookGenreDeleteView.as_view(), name="delete_book_genre"),
    path('delete_music_genre/<pk>', views.MusicGenreDeleteView.as_view(), name="delete_music_genre"),
    path('delete_album/<pk>', views.AlbumDeleteView.as_view(), name="delete_album"),
    path('delete_singer/<pk>', views.SingerDeleteView.as_view(), name="delete_singer"),
    path('delete_author/<pk>', views.AuthorDeleteView.as_view(), name="delete_author"),
    path('delete_director/<pk>', views.DirectorDeleteView.as_view(), name="delete_director"),
    path('delete_performer/<pk>', views.PerformerDeleteView.as_view(), name="delete_performer"),
]
app_name = 'recom'

