from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Review, Comment
from .serializers import ReviewSerializer, ReviewListSerializer, CommentSerializer
from django.http import JsonResponse
# from movies.models import UserRank


@api_view(['GET', 'DELETE'])
def review_detail_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'DELETE':
        if request.user == review.user:
            review.delete()
            # request.user.user_rank.remove(request.user)
            return JsonResponse({'message':'게시글이 삭제되었습니다.', 'success': True })
        else:
            return JsonResponse({'message':'게시글을 작성한 유저만 삭제할 수 있습니다.', 'success': False })
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
def comment_list(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    serializer = CommentSerializer(review.comment_set, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def comments_delete(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
        return JsonResponse({'message':'댓글이 삭제되었습니다.', 'success': True })
    else:
        return JsonResponse({'message':'댓글을 작성한 유저만 삭제할 수 있습니다.', 'success': False })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_review(request, review_pk):
   
    review = get_object_or_404(Review, pk=review_pk)
    if review.user == request.user:
        serializer = ReviewSerializer(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    return Response(False)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_comment(request,comment_pk):
    
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user == request.user:
        serializer = CommentSerializer(data=request.data, instance=comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    return Response(False)