# django
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Q

# rest_framework
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import status

# created Model, Serializers
from .models import Movie, Genre
from .serializers import MovieSerializer, MovieDetailSerializer, UserRankSerializer


# python tool
# from itertools import chain
import random
import time
from decouple import config
import requests

# module path
from reviews.serializers import ReviewListSerializer, ReviewSerializer

@api_view(['GET'])
def index(request):
    movies_popular = Movie.objects.values('title','backdrop_path','pk').order_by('-popularity')[:100]
    movies_popular = random.sample(list(movies_popular),20)
    movies_recent = Movie.objects.values('title','backdrop_path','pk').order_by('-release_date')[:100]
    movies_recent = random.sample(list(movies_recent),20)
    movies = movies_popular + movies_recent
    #queryset = chain(movies_popular,movies_recent)
    print( request.user) # 만약 유저명이 annoymous일 경우를 생각, 어떻게 인증을 검증할 지?
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

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
# @permission_classes([IsAuthenticated]) # token을 보내서 request.user하면 된당
def like_state(request, movie_pk, user_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk)
    state = user.like_movies.filter(pk=movie_pk).exists()
    return Response(state)

@api_view(['GET'])
@permission_classes(['IsAdminUser'])
def get_movies(request):
    api_key=config('API_KEY')
    for number in range(1,1000):
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
def review_create(request, movie_pk):
    if request.user.user_rank.filter(id=movie_pk).exists():
        content = '리뷰는 하나만 작성가능합니다.'
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data)

@api_view(['GET'])
def recommendation(request):
    user = request.user
    user_liked = user.like_movies.values('pk')
    list_pk = [liked['pk'] for liked in user_liked]
    movies = Movie.objects.order_by('-popularity').filter(~Q(pk__in=list_pk))
    print(movies)
    movies = random.sample(list(movies)[:100], 20)
   
    serializer = MovieDetailSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_rank(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = UserRankSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data)