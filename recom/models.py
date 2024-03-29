from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

# Create your models here.
from django.urls import reverse


class User(AbstractUser):
    birthday = models.DateField(null=True, verbose_name="Birthday")
    profile_photo = models.ImageField(upload_to="profile_photos", default="profile_photos/default_profile.png",
                                      verbose_name="Profile Photo")
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    info = models.TextField(blank=True, max_length=250)

    def get_absolute_url(self):
        return reverse('recom:user_detail', kwargs={"pk": self.pk})

    def get_ordered_comments(self):
        return self.comments.order_by('-date')


class PieceBaseModel(models.Model):
    name = models.CharField(null=False, max_length=100, verbose_name="Piece Name")
    publish_date = models.DateField(null=False, verbose_name="Publish Date")
    photo = models.ImageField(upload_to="piece_photos", default="piece_photos/default_piece.jpg",
                              verbose_name="Photo")
    text = models.TextField(null=True, verbose_name="Description")
    wished_by = models.ManyToManyField(to=User, related_name="wishes", blank=True)

    def __str__(self):
        return self.name

    def get_ordered_comments(self):
        return self.comments.order_by('-date')


class Point(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="points", verbose_name="User")
    piece = models.ForeignKey(to=PieceBaseModel, on_delete=models.CASCADE, related_name="points", verbose_name="Piece")
    point = models.IntegerField(null=False, verbose_name="Point")
    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "piece",)

    def __str__(self):
        return "{} - {} - {}".format(self.piece.name, self.user.get_full_name(), self.point)


class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments", verbose_name="User")
    piece = models.ForeignKey(to=PieceBaseModel, on_delete=models.CASCADE, related_name="comments",
                              verbose_name="Piece")
    text = models.TextField(null=False, max_length=500, verbose_name="Comment")
    liked = models.ManyToManyField(to=User, related_name="liked_comments", verbose_name="Liked by", blank=True)
    point = models.IntegerField(verbose_name="Point", blank=True, null=True)
    date = models.DateTimeField(auto_now=True)


class Author(models.Model):
    first_name = models.CharField(null=False, max_length=100, verbose_name="First Name")
    last_name = models.CharField(null=False, max_length=100, verbose_name="Last Name")
    photo = models.ImageField(upload_to="author_photos", default="author_photos/default_author.jpg",
                              verbose_name="Photo")

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class BookGenre(models.Model):
    name = models.CharField(null=False, max_length=50, verbose_name="Genre Name")

    def __str__(self):
        return self.name


class Book(PieceBaseModel):
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name="books")
    genre = models.ForeignKey(to=BookGenre, on_delete=models.CASCADE, related_name="books")


class Director(models.Model):
    first_name = models.CharField(null=False, max_length=100, verbose_name="First Name")
    last_name = models.CharField(null=False, max_length=100, verbose_name="Last Name")
    photo = models.ImageField(upload_to="director_photos", default="director_photos/default_director.jpg",
                              verbose_name="Photo")

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)


class MovieGenre(models.Model):
    name = models.CharField(null=False, max_length=50, verbose_name="Genre Name")

    def __str__(self):
        return self.name


class Performer(models.Model):
    first_name = models.CharField(null=False, max_length=100, verbose_name="First Name")
    last_name = models.CharField(null=False, max_length=100, verbose_name="Last Name")
    photo = models.ImageField(upload_to="performer_photos", default="performer_photos/default_performer.jpg",
                              verbose_name="Photo")

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.get_full_name()


class Movie(PieceBaseModel):
    director = models.ForeignKey(to=Director, on_delete=models.CASCADE, related_name="movie")
    genre = models.ForeignKey(to=MovieGenre, on_delete=models.CASCADE, related_name="movie")
    acted_by = models.ManyToManyField(to=Performer, related_name="acts", blank=True)


class Singer(models.Model):
    first_name = models.CharField(null=False, max_length=100, verbose_name="First Name")
    last_name = models.CharField(null=False, max_length=100, verbose_name="Last Name")
    photo = models.ImageField(upload_to="singer_photos", default="singer_photos/default_singer.jpg",
                              verbose_name="Photo")

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Album(models.Model):
    name = models.CharField(null=False, max_length=100, verbose_name="Album Name")
    publish_date = models.DateField(null=False, verbose_name="Publish Date")
    photo = models.ImageField(upload_to="album_photos", default="album_photos/default_album.jpg",
                              verbose_name="Photo")
    singer = models.ForeignKey(to=Singer, on_delete=models.CASCADE, related_name="album")

    def __str__(self):
        return self.name


class MusicGenre(models.Model):
    name = models.CharField(null=False, max_length=50, verbose_name="Genre Name")

    def __str__(self):
        return self.name


class Music(PieceBaseModel):
    album = models.ForeignKey(to=Album, on_delete=models.CASCADE, related_name="music")
    genre = models.ForeignKey(to=MusicGenre, on_delete=models.CASCADE, related_name="music")
