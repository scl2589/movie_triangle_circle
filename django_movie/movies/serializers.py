from rest_framework import serializers
# from accounts.serializers import UserSerializer
from .models import Movie, Genre, UserRank, RecommandMovie, GenreReview

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title','backdrop_path','pk',]

class MovieDetailSerializer(serializers.ModelSerializer):
    # d = { x.id:x.name for x in Genre.objects.all()}
    # genres = [ ]
    # date = serializers.DateTimeField(format="%Y")
    class Meta:
        model = Movie
        fields = '__all__' 
        
class UserRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRank
        fields = ['rank']


class SearchSerializer(serializers.ModelSerializer):
    like_user = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = ['title', 'backdrop_path', 'id', 'poster_path','like_user']
    def get_like_user(self, obj):
        return obj.like_users.count()

class RecommandMovieSerializer(serializers.ModelSerializer):
    # movies = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = ['movies']
    # def get_movies(self,obj):
    #     print(obj.movie)
    #     return obj.movie

class GenreSerializer(serializers.ModelSerializer):
    genrereview_set = serializers.SerializerMethodField()
    class Meta:
        model = Genre
        fields = ['id', 'name', 'genrereview_set']
    def get_genrereview_set(self, obj):
        return [{'id':x.id,'username':x.username,'content':x.content,} for x in obj.genrereview_set.all()][::-1]
class GenreReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreReview
        fields = ['id','content','username']
    