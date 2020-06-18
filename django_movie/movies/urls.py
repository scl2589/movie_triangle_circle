from django.urls import path, include
from . import views
app_name = 'movies'

urlpatterns = [
    # 영화 장르별 
    # path('', views.genre_list),
    # 리뷰 관련
    path('<int:movie_pk>/reviews/', views.review_index),
    path('<int:movie_pk>/reviews/create/', views.review_create),

    # 영화 관련 
    path('', views.index, name='movie_list'),
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    
    # 영화 장르게시판
    path('genres/', views.get_genre),
    path('<int:genre_pk>/gcomment/', views.getGreview_createGreview),

    # 영화 좋아요
    path('<int:movie_pk>/like/', views.like ),
    path('<int:movie_pk>/<int:user_pk>/like/', views.like_state),

    # 영화 요청
    path('getmovie/', views.get_movies),

    # 영화 회원가입 추천
    path('user/recommendation/', views.recommendation),
    # 영화 로그아웃 추천
    path('createrecommend/<int:user_pk>/', views.create_recommend),

    # 영화 랭크 (평점)
    # path('<int:movie_pk>/rank/', views.create_rank),
    
    # array
    # path('getusercollob/', views.colloborative_filter),
    path('getrecommend/<int:user_id>/', views.get_user_recommend),
    # path('recommendmovie/<int:user_id>/', views.get_user_recommend_movie)
]