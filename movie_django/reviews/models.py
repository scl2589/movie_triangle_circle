from django.db import models
from django.conf import settings
# class Genre(models.Model):
#     name = models.CharField(max_length=100)

# class Movie(models.Model):
#     movie_cd = models.CharField(max_length=100)
#     title_kr = models.CharField(max_length=100)
#     title_en = models.CharField(max_length=100)
#     open_date = models.DateField()
#     # type_num = models.CharField(max_length=100)
#     # prdt_stat = models.CharField(max_length=100)
#     nation = models.CharField(max_length=100)
#     # rep_genre = models.CharField(max_length=100)
#     directors = models.CharField(max_length=100)
#     popularity = models.FloatField()
#     adult = models.BooleanField()
#     overview = models.TextField()
#     original_language = models.CharField(max_length=100)
#     poster_path = models.CharField(max_length=300)

#     genres = models.ManyToManyField(Genre,related_name='genre_movies')
#     like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')

class Review(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.TextField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
