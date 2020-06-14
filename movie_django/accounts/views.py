from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserProfileSerializer
from movies.models import Movie
from reviews.models import Review
from movies.serializers import MovieSerializer
from django.contrib.auth.decorators import login_required
User = get_user_model()
# Create your views here.
@api_view(['GET'])
def profile(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)


# @api_view(['GET']) # 삭제될 예정
# # @permission_classes([IsAuthenticated])
# def get_user_id(request, username):
#     return Response(User.objects.filter(username=username)[0].id)

@login_required
def follow(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=pk)
    if user != request.user:
        if user.followers.filter(pk=request.user.pk).exists():
            user.followers.remove(request.user)
        else:
            user.followers.add(request.user)
    return redirect('accounts:detail', user.pk)


@api_view(['GET']) 
def user_info(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    
    # list_pk = [liked.pk for liked in user.like_movies.all()]
    # movies = Movie.objects.filter(pk__in=list_pk)
    serializer = UserProfileSerializer(user)
   
    return Response(serializer.data)

