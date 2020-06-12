from django.urls import path
from . import views

name = 'accounts'

urlpatterns = [
    path('<int:user_pk>/', views.profile),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    path('<username>/',views.get_user_id),
]
