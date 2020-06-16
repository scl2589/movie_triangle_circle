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




@api_view(['GET']) 
def user_info(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    
    # list_pk = [liked.pk for liked in user.like_movies.all()]
    # movies = Movie.objects.filter(pk__in=list_pk)
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def follow(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    if user != request.user: # 본인 여부
        if user.followers.filter(pk=request.user.pk).exists():
            user.followers.remove(request.user) # 팔로우 제거
        else:
            user.followers.add(request.user) # 팔로우 추가
    
    return Response({'success':True})


@api_view(['GET'])
def checkFollow(request, user_pk, authenticated_pk):
    user = get_object_or_404(User, pk=user_pk)
    state = user.followers.filter(pk=authenticated_pk).exists()
    return Response(state)
