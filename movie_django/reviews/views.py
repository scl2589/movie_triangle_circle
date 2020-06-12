from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Review, Comment
from .serializers import ReviewSerializer, ReviewListSerializer, CommentSerializer
import os, sys
path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path)
from movies.models import Movie

@api_view(['GET'])
def index(request,movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.review_set.order_by('-pk')
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data)


@api_view(['GET'])
def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    serializer = ReviewSerializer(review)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comments_create(request, review_pk):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, review_id=review_pk)
        return Response(serializer.data)
