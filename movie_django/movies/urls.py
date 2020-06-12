from django.urls import path, include
from . import views
app_name = 'movies'

urlpatterns = [
    path('<int:movie_pk>/reviews/', views.review_index),
    path('<int:movie_pk>/reviews/create/', views.create),
    path('', views.index, name='movie_list'),
    path('selection/', views.selection, name='movie_selection'),
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_pk>/like/', views.like ),
    path('<int:movie_pk>/<int:user_pk>/like/', views.like_state),
    # 영화 요청
    path('getmovie/', views.get_movies),
]