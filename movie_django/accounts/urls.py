from django.urls import path
from . import views

name = 'accounts'

urlpatterns = [
    path('<int:user_pk>/', views.profile),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    path('<int:user_pk>/follow/<int:authenticated_pk>/', views.checkFollow),
    # path('<username>/',views.get_user_id),
    path('<int:user_pk>/info/', views.user_info),
]
