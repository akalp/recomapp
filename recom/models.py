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