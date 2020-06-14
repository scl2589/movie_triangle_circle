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
    like = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields= ('id','like','reviews','username') 
    def get_like(self, obj):  # "get_" + field name
        
        return obj.like_movies.values_list('title', flat=True)
    def get_reviews(self,obj):
        
        # print([x.movie for x in obj.review_set.all()])
        # for x in obj.review_set.all():
            
        #     try: 
        #         print(x.movie.title)
            
        #     except:
        #         print(x.id)
        # return obj.review_set.values_list('title',flat=True)
        return [x.movie.title for x in obj.review_set.all()]

