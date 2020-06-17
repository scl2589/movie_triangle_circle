from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('<int:review_pk>/', views.review_detail_delete, name='detail_delete'),
    path('<int:review_pk>/comment_create/', views.comments_create, name='comment_create'),
    path('<int:review_pk>/get_comments/', views.comment_list),
    path('<int:review_pk>/comment_delete/<int:comment_pk>', views.comments_delete),
    path('<int:review_pk>/update_review/',views.update_review),
    path('update_comment/<int:comment_pk>/', views.update_comment),
]