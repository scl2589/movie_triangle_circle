from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_auth.models import TokenModel


# from reviews.serializers import ReviewListSerializer
from movies.models import Movie

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','like_movies','comment_set', 'review_set', 'user_rank')


class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = TokenModel
        fields = ('key', 'user')

# class UserProfileSerializer(serializers.ModelSerializer):
#     # user = UserSerializer(many=True)
#     review = ReviewListSerializer(many=True)
#     class Meta:
#         model = Movie
#         fields= ('title','user','review') 