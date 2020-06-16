
from django.contrib import admin
from django.urls import path, include
from movies import views as m_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('movies/', include('movies.urls')),
    # 직접 만든 적은 없지만 rest_auth라는 앱이 생긴다.
    # 로그인 & 로그아웃
    path('rest-auth/', include('rest_auth.urls')),
    # 회원가입
    path('rest-auth/signup/', include('rest_auth.registration.urls')),
    path('accounts/', include('accounts.urls')),
    path('reviews/', include('reviews.urls')),
    # 검색
    path('search/',m_views.search)

]