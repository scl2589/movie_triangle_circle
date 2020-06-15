<template>
  <div>
    <div class="header">
      <h1> {{userInfo.username}} </h1>
    </div>
    <!-- 좋아한 영화 -->
    <div class="d-flex justify-content-center"> 
      <ul class="nav d-flex align-items-end" id="nav-tab" role="tablist">
        <li class="nav-item" role="presentation" :class="{active: like}">
          <p class="nav-link" @click="clickLike"><i class="fas fa-heart mr-1"></i>좋아요한 영화</p>
        </li>
        <li class="nav-item" role="presentation" :class="{active: review}" >
          <p class="nav-link" @click="clickReview"><i class="fas fa-pencil-alt mr-1"></i>작성한 리뷰 </p>
        </li>
      </ul>
    </div>
    <UserProfileLiked :userInfo="userInfo" v-show="clickedLiked" />
    <UserProfileReview :userInfo="userInfo" v-show="clickedReview"/>



    <!--userInfo = id, username, like_movies, comment_set, review_set -->
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'
import UserProfileLiked from '@/views/accounts/UserProfileLikedView.vue'
import UserProfileReview from '@/views/accounts/UserProfileReviewView.vue'

export default {
  name: 'UserProfile',
  data () {
    return {
      userInfo: [],
      posterPaths: [],
      like: true,
      review: false,
      clickedLiked: true,
      clickedReview: false,
    }
  },
  components: {
    UserProfileLiked,
    UserProfileReview,
  },
  // 로그인 했을 때 자기 자신의 정보
  methods: {
    clickLike(){
      this.clickedReview = false;
      this.clickedLiked = true;
      this.like = true;
      this.review = false;
    },
    clickReview(){
      this.clickedLiked = false;
      this.clickedReview = true;
      this.like = true;
      this.review = false;
    }
  },
  created() {
    axios.get(SERVER.URL + '/accounts/'+this.$route.params.userId + '/info/')
    .then(res => {
      this.userInfo = res.data
      // console.log(this.userInfo.reviews.movie_rank.length)
      // if (this.userInfo.reviews.movie_rank.length){
      //   this.userInfo.reviews.movie_rank = this.userInfo.reviews.movie_rank[0].rank
      // }
      res.data.like.forEach( movie => {
        movie.poster_path=SERVER.IMAGEPATH.imagepath780 + movie.poster_path
      })
    })
    .catch(err => console.log(err))
  },
  mounted() {
  },
}
</script>

<style scoped>
p{
  margin: 0;
}

#nav a {
  font-weight: bold;
  color: #345389;
}

#nav a.router-link-exact-active {
  color: #f5b893;
}

a.nav-link{
  color: #345389;
  text-align:end;
}

.active {
  color: #f5b893 !important; 
}

.fa-heart {
  color: red;
}

.fa-pencil-alt {
  color: black;
}

#nav-tab {
  cursor: pointer;
}

</style>