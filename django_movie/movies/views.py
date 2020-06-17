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
from .models import Movie, Genre, UserRank, RecommandMovie
from .serializers import MovieSerializer, MovieDetailSerializer, UserRankSerializer, SearchSerializer, RecommandMovieSerializer, GenreSerializer


# python tool
# from itertools import chain
import random
import time
from decouple import config
import requests
import re

# module path
from reviews.serializers import ReviewListSerializer, ReviewSerializer

User = get_user_model()
genres_list = list(Genre.objects.values_list('name',flat=True))

@api_view(['GET'])
def index(request):
    movies_popular = Movie.objects.values('title','backdrop_path','pk').order_by('-popularity')[:100]
    movies_popular = random.sample(list(movies_popular),20)
    movies_recent = Movie.objects.values('title','backdrop_path','pk').order_by('-release_date')[:100]
    movies_recent = random.sample(list(movies_recent),20)
    movies = movies_popular + movies_recent
    
    if request.user.username:
        user = request.user
        RM = user.recommandmovie_set.order_by('-coef')[:20] #오름차순이다.
        RMs = [ x.movie for x in RM]
        random.shuffle(RMs)
        movies.extend(RMs)
    
    #queryset = chain(movies_popular,movies_recent)
    # 만약 유저명이 annoymous일 경우를 생각, 어떻게 인증을 검증할 지?
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
    
    UserRank.objects.create(user=request.user, movie=movie,rank =request.data['rank'])
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data)

## 추천 알고리즘 , 그냥 행렬곱하자
# @api_view(['GET']) # accecpted render response error
def colloborative_filter(user_id):
    movie_data = Movie.objects.all()
    user_data = User.objects.all()
    ur = UserRank.objects.all()
    # arr = [[0]*(len(movie_data)) for _ in range(len(movie_data))]
    for u in user_data:
        ms = u.user_rank.all()
        for i in range(len(ms)):
            for j in range(i+1,len(ms)):
                cus = ms[i].rank_users.all() & ms[j].rank_users.all()
                temp = []
                for cu in cus:
                    a = ms[i].userrank_set.filter(user_id=cu.id)[0].rank
                    b = ms[j].userrank_set.filter(user_id=cu.id)[0].rank
                    temp.append((a,b))
                up=0
                d1=0
                d2=0
                for a,b in temp:
                    up+=a*b
                    d1+=a**2
                    d2+=b**2
                if d1+d2 == 0:
                    result =0 
                else:
                    result = up/(d1**(1/2) + d2**(1/2))
                    recomv = RecommandMovie.objects.filter(movie_id=movie.id, user_id=user_id)[0]
                    recomv.coef = result+recomv.coef
                    recomv.save()
    # 장르의 가중치를 구해놓음                
                # Recommand.objects.create(movie1_id=m[i].id,movie2_id=m[j].id,result=result)
    #             serializer = RecommandSerializer(Recommand,data=result)
    #             if serializer.is_valid():
    #                 serializer.save(movie1_id=m[i].id,movie2_id=m[j].id)
    # return Response({"message":"success"})
    # return data 피어슨 계수


# 1. 처음 회원가입시 받은 유저의 좋아요 개수를 이요해서 장르에 w를 부여하고 모든 영화에 대한 coefficient를 구해서 이 수치가 높은 영화들을 추천 20~30
# 2. 선택한 영화와 유사한 장르의 영화를 선호했던 영화의 데이터를 이용해서 추천
# 3. 이 영화를 평가한 유저의 평점을 이용한 collaborative filtering
# 4. 좋야요한 영화의 평점을 기반으로 한 영화 추천
# 5. 연령대, 성별 등등


@api_view(['GET']) # 유저가 처음 회원가입할 때만 동작하고 그 뒤에는 유저의 활동량에 따라 업데이트해줄지를 결정
def get_user_recommend(request,user_id):
    user = get_object_or_404(User, pk=user_id)
    lmovies = user.like_movies.all() # 좋아요한 영화들
    
    genres_dict = { x:0 for x in genres_list } # 좋아요한 영화들의 장르 개수를 구함 여기서 숫자가 높은 걸 선택해서 그 장르만 돌림
    print(genres_dict)
    for l in lmovies:
        for g in l.genres.all():
            genres_dict[g.name]+=1
    # movies = Movie.objects.all() # 모든 영화들의 coefficient 구함, 엄~청 오래걸림 O(n*g), n: 영화 개수, g: 장르 개수 2500개,
    # 장르별 top 30*19
    movies = Movie.objects.order_by('-popularity')[:500]
    print(genres_dict)
    for movie in movies:
        up =0
        down = 0
        for x in movie.genres.all():
            if genres_dict.get(x.name,0):
                up+=genres_dict[x.name]
                down+=((genres_dict[x.name]**(2)))
        if down:    
            coef = up/(down**(1/2)+3**(1/2))
            if coef:
                RecommandMovie.objects.create(movie_id=movie.id, user_id=user.id, coef=coef) # 일정 점수 이하일 경우 삭제
    print('success')
    return Response({'success':True})
    
# @api_view(['GET'])
# def get_user_recommend_movie(request,user_id):
#     user = get_object_or_404(User,pk=user_id)
#     RM = user.recommandmovie_set.order_by('-coef')[:20] # 장고 기본 정렬순서는 오름차순이다.
#     RMs = [ x.movie for x in RM]
#     serializer = MovieSerializer(RMs, many=True)
#     return Response(serializer.data)


@api_view(['GET'])
def recommendation(request): # 회원가입 시 보여주는 영화
    user = request.user
    user_liked = user.like_movies.values('pk')
    list_pk = [liked['pk'] for liked in user_liked]
    movies = Movie.objects.order_by('-popularity').filter(~Q(pk__in=list_pk))
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

# def genre_list(request):
#     movies = Movie.objects.order_by('-popularity').filter()
#     pass


# search

@api_view(['GET'])
def search(request):
    
    q = request.GET.get('query')
    if q:
        movie = Movie.objects.filter(Q(title__icontains=q) | Q(original_title__icontains=q) | Q(overview__icontains=q)) # 해리 포터
        if movie:
            serializer = SearchSerializer(movie, many=True)
            return Response(serializer.data)
    
    return Response({'message': '검색결과가 없습니다.'})


# tag 만들어야지, original title


@api_view(['GET'])
def get_genre(request):
    g = Genre.objects.all()
    print(g)
    serializer = GenreSerializer(g, many=True)
    return Response(serializer.data)