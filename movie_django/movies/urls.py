from django.urls import path, include
from . import views
app_name = 'movies'

urlpatterns = [
    # 리뷰 관련
    path('<int:movie_pk>/reviews/', views.review_index),
    path('<int:movie_pk>/reviews/create/', views.create),

    #영화 관련 
    path('', views.index, name='movie_list'),
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_pk>/like/', views.like ),
    path('<int:movie_pk>/<int:user_pk>/like/', views.like_state),
    # 영화 요청
    path('getmovie/', views.get_movies),
    # 영화 추천
    path('user/recommendation/', views.recommendation),
]