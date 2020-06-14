<template>
  <div>
    <h1> {{userInfo.username}} </h1>
    <!-- 좋아한 영화 -->
    <h2>좋아요한 영화</h2>
    <div v-for="like_movie in userInfo.like_movies" :key="`liked_${like_movie}`">
      <p>{{like_movie}}</p>
    </div>
    <!-- 작성한 리뷰 -->
    {{userInfo}}
    <!--userInfo = id, username, like_movies, comment_set, review_set -->
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'
export default {
  name: 'UserProfile',
  data () {
    return {
      userInfo: [],
    }
  },
  // 로그인 했을 때 자기 자신의 정보
  methods: {

  },
  created() {
    console.log(SERVER.URL + '/accounts/'+this.$route.params.userId + '/info/')
    axios.get(SERVER.URL + '/accounts/'+this.$route.params.userId + '/info/')
    .then(res => this.userInfo = res.data)
    .catch(err => console.log(err))
  }
}
</script>

<style>

</style>