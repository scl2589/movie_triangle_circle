<template>
  <div class="container">
    <div class="header mb-0 ">
      <div class="row justify-content-center mb-3">
        <h2> 
          {{userInfo.username}} 
          <span><button class="btn btn-sm" >팔로우</button></span>
        </h2>
      </div>
      <div class="row justify-content-between setWidth mb-3">
        <!-- <p> -->
          <span>리뷰 수 {{userInfo.reviews.length }}</span>
          <span>팔로워 {{userInfo.followers.length }}</span>
          <span>팔로우 {{userInfo.followings.length}}</span>
        <!-- </p> -->
      </div>
    </div>
    <!-- 좋아한 영화 -->
    <div class="d-flex justify-content-center line"> 
      <ul class="nav d-flex align-items-end" id="nav-tab" role="tablist">
        <li class="nav-item" role="presentation" :class="{active: isLike}">
          <p class="nav-link" @click="clickLike"><i class="fas fa-heart mr-1"></i>좋아요 누른 영화</p>
        </li>
        <li class="nav-item" role="presentation" :class="{active: isReview}" >
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
      isLike: true,
      isReview: false,
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
      // this.isLike = true;
      // this.isReview = false;
      this.clickedReview = false;
      this.clickedLiked = true;
    },
    clickReview(){
      // this.isLike = true;
      // this.isReview = false;
      this.clickedLiked = false;
      this.clickedReview = true;
      
    }
  },
  created() {
    axios.get(SERVER.URL + '/accounts/'+this.$route.params.userId + '/info/')
    .then(res => {
      this.userInfo = res.data
      res.data.like.forEach( movie => {
        movie.poster_path=SERVER.IMAGEPATH.imagepath780 + movie.poster_path
      })
    })
    .catch(err => console.log(err))
  },
  updated(){
    if(this.clickedLiked ===true){
      this.isLike = true
      this.isReview = false
    }
    if(this.clickedReview === true){
      this.isReview = true
      this.isLike = false
    } 
  }
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
  border-top: 1px solid #8e8e8e;
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

.line {
  /* border-bottom-style: solid; */
  border-top: 1px solid #dbdbdb;
}

.setWidth{
  width: 30%;
  margin: auto;
}

.btn:hover {
  color: white;
}
</style>