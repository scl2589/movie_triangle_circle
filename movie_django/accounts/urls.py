from django.urls import path
from . import views
from movies import views as m_views
name = 'accounts'

urlpatterns = [
    path('<int:user_pk>/', views.profile),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    # path('<username>/',views.get_user_id),
    path('<int:user_pk>/info/', views.user_info),
    # 검색
    path('search/',m_views.search)
]
