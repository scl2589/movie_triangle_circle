from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')
    # age = models.IntegerField(null=True)
    # favor_genres = models.TextField(blank=True)
    # gender = models.BooleanField(default=0)