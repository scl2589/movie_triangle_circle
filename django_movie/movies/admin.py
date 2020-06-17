from django.contrib import admin
from .models import Movie, UserRank, RecommandMovie, GenreReview
# Register your models here.
admin.site.register(Movie)
admin.site.register(UserRank)
admin.site.register(RecommandMovie)
admin.site.register(GenreReview)