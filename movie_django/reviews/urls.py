from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    
    path('<int:review_pk>/', views.detail, name='detail'),
    path('<int:review_pk>/comment_create/', views.comments_create, name='comment_create'),
    path('<int:review_pk>/get_comments/', views.get_comments),
]