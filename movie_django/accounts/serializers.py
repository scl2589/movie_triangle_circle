from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_auth.models import TokenModel

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','like_movies','comment_set', 'review_set')



class TokenSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = TokenModel
        fields = ('key', 'user')