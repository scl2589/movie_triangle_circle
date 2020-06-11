from django.urls import path, include
from . import views
app_name = 'movies'

urlpatterns = [
    path('reviews/', include('reviews.urls')),
    path('', views.index, name='movie_list'),
    path('selection/', views.selection, name='movie_selection'),
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('int:movie_pk>/', views.like ),
    # 영화 요청
    path('getmovie/', views.get_movies)
]