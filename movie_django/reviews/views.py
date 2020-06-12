from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Review, Comment
from .serializers import ReviewSerializer, ReviewListSerializer, CommentSerializer
from django.http import JsonResponse


@api_view(['GET', 'DELETE'])
def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'DELETE':
        if request.user == review.user:
            review.delete()
            return JsonResponse({'message':'게시글이 삭제되었습니다.' })
        else:
            return JsonResponse({'message':'게시글을 작성한 유저만 삭제할 수 있습니다.' })
    else:
        serializer = ReviewSerializer(review)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comments_create(request, review_pk):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, review_id=review_pk)
        return Response(serializer.data)

@api_view(['GET'])
def get_comments(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    serializer = CommentSerializer(review.comment_set, many=True)
    return Response(serializer.data)
