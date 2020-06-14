<template>
  <div>
    <div class="header">
      <h1> {{userInfo.username}} </h1>
    </div>
    <!-- 좋아한 영화 -->
    
    <h2>좋아요한 영화</h2>
    <!-- <div v-for="like_movie in userInfo.like" :key="`liked_${like_movie}`"> -->
      <p>{{ userInfo.like }}</p>
    <!-- </div> -->
    <div v-for="posterpath in posterPaths" :key="posterpath">
      <img :src="posterpath" alt="영화포스터">
    </div>



    <ul class="nav nav-tabs d-flex align-items-end" id="nav-tab" role="tablist">
      <li class="nav-item" role="presentation">
        <p class="nav-link">좋아요 </p>
      </li>
      <li class="nav-item" role="presentation">
        <p class="nav-link">작성한 리뷰 </p>
      </li>
    </ul>
    <UserProfileLiked :userInfo="userInfo" :posterPaths="posterPaths" v-show="clickedLiked" />
    <UserProfileReview v-show="clickedReview"/>



    <!-- 작성한 리뷰 -->
    <h2>리뷰를 작성한 영화</h2>
    {{userInfo.reviews}}
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

      clickedLiked: true,
      clickedReview: true,
    }
  },
  components: {
    UserProfileLiked,
    UserProfileReview,
  },
  // 로그인 했을 때 자기 자신의 정보
  methods: {

  },
  created() {
    axios.get(SERVER.URL + '/accounts/'+this.$route.params.userId + '/info/')
    .then(res => {
      this.userInfo = res.data
      res.data.poster.forEach( url => {
        this.posterPaths.push(SERVER.IMAGEPATH.imagepath780 + url)
      })
      })
    .catch(err => console.log(err))
  }
}
</script>

<style>

</style>