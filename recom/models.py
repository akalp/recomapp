from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    birthday = models.DateField(null=True, verbose_name="Birthday")
    profile_photo = models.ImageField(upload_to="profile_photos", default="profile_photos/default_profile.jpg", verbose_name="Profile Photo")


class PieceBaseModel(models.Model):
    name = models.CharField(null=False, max_length=100, verbose_name="Piece Name")
    publish_date = models.DateField(null=False, verbose_name="Publish Date")
    photo = models.ImageField(upload_to="piece_photos", default="piece_photos/default_piece.jpg",
                              verbose_name="Photo")
    text = models.TextField(null=True, verbose_name="Description")
    wished_by = models.ManyToManyField(to=User, related_name="wishes")


class Point(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="points", verbose_name="User")
    piece = models.ForeignKey(to=PieceBaseModel, on_delete=models.CASCADE, related_name="points", verbose_name="Piece")
    point = models.IntegerField(null=False, verbose_name="Point")

    class Meta:
        unique_together = ("user", "piece",)


class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments", verbose_name="User")
    piece = models.ForeignKey(to=PieceBaseModel, on_delete=models.CASCADE, related_name="points", verbose_name="Piece")
    text = models.TextField(null=False, max_length=500, verbose_name="Comment")
    liked = models.ManyToManyField(to=User, related_name="liked_comments", verbose_name="Liked by")

    class Meta:
        unique_together = ("user", "piece",)


class Author(models.Model):
    first_name = models.CharField(null=False, max_length=100, verbose_name="First Name")
    last_name = models.CharField(null=False, max_length=100, verbose_name="Last Name")
    photo = models.ImageField(upload_to="author_photos", default="author_photos/default_author.jpg",
                              verbose_name="Photo")


class BookGenre(models.Model):
    name = models.CharField(null=False, max_length=50, verbose_name="Genre Name")


class Book(PieceBaseModel):
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name="books")
    genre = models.ForeignKey(to=BookGenre, on_delete=models.CASCADE, related_name="books")


class Singer(models.Model):
    first_name = models.CharField(null=False, max_length=100, verbose_name="First Name")
    last_name = models.CharField(null=False, max_length=100, verbose_name="Last Name")
    photo = models.ImageField(upload_to="singer_photos", default="singer_photos/default_singer.jpg",
                              verbose_name="Photo")


class Album(models.Model):
    name = models.CharField(null=False, max_length=100, verbose_name="Album Name")
    publish_date = models.DateField(null=False, verbose_name="Publish Date")
    photo = models.ImageField(upload_to="album_photos", default="album_photos/default_album.jpg",
                              verbose_name="Photo")
    singer = models.ForeignKey(to=Singer, on_delete=models.CASCADE, related_name="album")


class MusicGenre(models.Model):
    name = models.CharField(null=False, max_length=50, verbose_name="Genre Name")


class Music(PieceBaseModel):
    album = models.ForeignKey(to=Album, on_delete=models.CASCADE, related_name="music")
    genre = models.ForeignKey(to=MusicGenre, on_delete=models.CASCADE, related_name="music")
