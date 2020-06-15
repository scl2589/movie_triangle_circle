from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_auth.models import TokenModel
from django.db import models
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
    # poster = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields= ('id','like','reviews','username') 
    def get_like(self, obj):  # "get_" + field name
        # print(User.objects.prefetch_related('comment_set'))
        movies = obj.like_movies.all()
     
        print(movies.annotate(like_count=models.Count('like_users')))
        a = movies.annotate(like_count=models.Count('like_users'))
        return a.values('id','title','poster_path','like_count')
    def get_reviews(self,obj):
        # print([x.movie for x in obj.review_set.all()])
        # for x in obj.review_set.all():
            
        #     try: 
        #         print(x.movie.title)
            
        #     except:
        #         print(x.id)
        # return obj.review_set.values_list('title',flat=True)
        # return obj.review_set.values('title')
        # 리뷰의 영화의 좋아요를 받은 개수, 리뷰
        review = obj.review_set.all()
        
        # print(User.objects.prefetch_related('comment_set'))
        # print(User.objects.first().comment_set.all())
        return {'movie_title': x.movie.title for x in review}
    def reviewposter(self, obj):
        
        return [x.movie.poster_path for x in obj.review_set.all()] 