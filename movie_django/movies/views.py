from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from .models import Movie,Genre
from .serializers import MovieSerializer, MovieDetailSerializer
from django.contrib.auth import get_user_model

from itertools import chain
import random
import time
from decouple import config
import requests

import os, sys
path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path)
from reviews.serializers import ReviewListSerializer, ReviewSerializer

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
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

@api_view(['GET'])
# @permission_classes(['IsAuthenticated'])
def like_state(request, movie_pk, user_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk)
    state = user.like_movies.filter(pk=movie_pk).exists()
    return Response(state)

@api_view(['GET'])
@permission_classes(['IsAdminUser'])
def get_movies(request):
    api_key=config('API_KEY')
    for number in range(1,10):
        total = []
        if number%50==0:
            print(number)
            time.sleep(10)
        print(number)
        url = f'https://api.themoviedb.org/3/movie/{number}?api_key={api_key}&query=whiplash&language=ko-KR&region=KR&append_to_response=include_image_language=ko,null'
        res = requests.get(url)
        if res.status_code == 200:
            total.append(res.json())
    print('get data')

    return Response({"message":"success"})


@api_view(['GET'])
def review_index(request,movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.review_set.order_by('-pk')
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data)