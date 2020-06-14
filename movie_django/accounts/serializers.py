from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_auth.models import TokenModel


from movies.models import Movie
# from reviews.serializers import ReviewListSerializer



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




class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields= ('user',) 


