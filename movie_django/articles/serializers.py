from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    created_at = serializers.DateTimeField(format="%Y년 %m월 %d일 %H:%M:%S",required=False)
    class Meta:
        model = Comment
        fields = ('content','user','id','created_at')
        
class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    created_at = serializers.DateTimeField(format="%Y년 %m월 %d일 %H:%M:%S")
    comment_set = CommentSerializer(required=False, many=True)
    class Meta:
        model = Article
        fields = ('id', 'title', 'user','created_at', 'content','comment_set')


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    created_at = serializers.DateTimeField(format="%Y년 %m월 %d일 %H:%M:%S", required=False)
    comment_set = CommentSerializer(required=False, many=True)
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

