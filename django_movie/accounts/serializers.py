from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_auth.models import TokenModel
from django.db import models
from movies.models import Movie, UserRank
# from reviews.serializers import ReviewListSerializer
from django.core.serializers.json import DjangoJSONEncoder 


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
    followersobj = serializers.SerializerMethodField()
    followingsobj = serializers.SerializerMethodField()
    # poster = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields= ('id','like','reviews','username','followers','followings','followersobj', 'followingsobj') 
    def get_like(self, obj):  # "get_" + field name
        # print(User.objects.prefetch_related('comment_set'))
        # print(movies.annotate(like_count=models.Count('like_users')))
        # a = movies.annotate(like_count=models.models.Count(Subquery(obj.like_movies)..values('id', 'title', 'poster_path','like_count')
        # print(models.Subquery(obj.like_movies).annotate(cnt=models.Count('like_users')).values('cnt'))
        # i=0
        # for x in obj.like_movies.all():
        #     print(a['like'])
            # a['like'][i]['like_count'] = x.like_users.all()
            # i+=1
        # .annotate(like_count=models.Count(F'like_users'))
        # lc = [{'like_count':[x.like_users.count()]} for x in obj.like_movies.all()]
        # return movies.values('id', 'title', 'poster_path')
        return [{'title':x.title,'id': x.id,'like':x.like_users.count(),'poster_path': x.poster_path}  for x in obj.like_movies.all()]
    def get_reviews(self,obj):
        
        review = obj.review_set.all()
        return  [{'review_title':x.title,'movie_title': x.movie.title,'movie_like':x.movie.like_users.count(),'movie_rank':x.movie.userrank_set.filter(user_id=obj.id)[0].rank, 'review_id':x.id}  for x in review]

    def get_followersobj(self, obj):
        serializer = UserSerializer(obj.followers.all(), many=True)
        return serializer.data

    def get_followingsobj(self, obj):
        serializer = UserSerializer(obj.followings.all(), many=True)
        return serializer.data