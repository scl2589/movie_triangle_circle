from django.contrib import admin
from .models import Movie, UserRank, RecommandMovie
# Register your models here.
admin.site.register(Movie)
admin.site.register(UserRank)
admin.site.register(RecommandMovie)