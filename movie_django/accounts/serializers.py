from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_auth.models import TokenModel
from django.db import models
from movies.models import Movie, UserRank
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
        return [{'review_title':x.title,'movie_title': x.movie.title,'movie_like':x.movie.like_users.count(),'movie_rank':UserRank.objects.filter(movie_id=x.movie.id,user_id=obj.id).values('rank')}  for x in review] # 나중에 고침
    def reviewposter(self, obj):
        
        return [x.movie.poster_path for x in obj.review_set.all()] 