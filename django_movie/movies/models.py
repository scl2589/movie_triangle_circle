
# Create your models here.
from django.db import models

from django.conf import settings
from django.apps import apps

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    adult = models.BooleanField()
    overview = models.TextField()
    original_language = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=200)
    backdrop_path = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre,related_name='genre_movies')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    rank_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_rank', through='UserRank')
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='recommand_movie', through='RecommandMovie' )
    director = models.CharField(max_length=100, null=True)
    actor = models.CharField(max_length=100, null=True)
    id = models.IntegerField(primary_key=True)


#     # new column    
#     # bookmark = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

#     # 추가해야할 필드?

class UserRank(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 유저가 삭제될 경우는 어떻게 해야하는가
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    # Review = apps.get_model('reviews', 'Review')
    # review = models.OneToOneField(Review, on_delete=models.CASCADE)
    rank = models.FloatField(default=0)


class RecommandMovie(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coef = models.FloatField(default=0)

class GenreReview(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Genre = models.ForeignKey(Movie, on_delete=models.CASCADE)
   