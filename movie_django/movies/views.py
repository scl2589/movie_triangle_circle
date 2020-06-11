from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from .models import Movie
from .serializers import MovieSerializer, MovieDetailSerializer
from itertools import chain
import random


@api_view(['GET'])
def index(request):
    movies_popular = Movie.objects.values('title','backdrop_path','pk').order_by('-popularity')[:100]
    movies_popular = random.sample(list(movies_popular),20)
    movies_recent = Movie.objects.values('title','backdrop_path','pk').order_by('-release_date')[:100]
    movies_recent = random.sample(list(movies_recent),20)
    movies = movies_popular + movies_recent
    #queryset = chain(movies_popular,movies_recent)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

def selection():
    pass

@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data)

def like(request, movie_pk):
    user = request.user 
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        liked = True
        # messages.info(request, ':)')
    else:
        movie.like_users.add(user)
        liked =False
        # messages.info(request, ':<')
    context = {
        'liked': liked,
        'count': movie.like_users.count(),
    }
    return JsonResponse(context)



@api_view(['POST'])
@permission_classes(['IsAdminUser'])
def get_movies(request):
    
    return Response(serializer.data)