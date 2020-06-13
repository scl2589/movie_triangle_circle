from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Movie,Genre

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title','backdrop_path','pk']

class MovieDetailSerializer(serializers.ModelSerializer):
    # d = { x.id:x.name for x in Genre.objects.all()}
    # genres = [ ]
    class Meta:
        model = Movie
        fields = '__all__'
        