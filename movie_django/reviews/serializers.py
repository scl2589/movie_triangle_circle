from rest_framework import serializers
from .models import Review, Comment
from accounts.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    class Meta:
        model = Comment
        fields = ('content','user','id','created_at')
        
class ReviewListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    comment_set = CommentSerializer(required=False, many=True)
    class Meta:
        model = Review
        fields = ('id', 'title', 'user','created_at', 'content','comment_set')

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    comment_set = CommentSerializer(required=False, many=True)
    movie_title = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at','comment_set', 'movie_title','movie')
    def get_movie_title(self, obj):  # "get_" + field name
        return obj.movie.title

    