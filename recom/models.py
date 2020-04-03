from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    birthday = models.DateField(null=True, verbose_name="Birthday")
    profile_photo = models.ImageField(upload_to="profile_photos", default="profile_photos/default_profile.jpg", verbose_name="Profile Photo")