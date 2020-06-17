<template>
  <div class="container">
    <div class="header mb-0 ">
      <div class="row justify-content-center mb-3">
        <h2> 
          {{userInfo.username}} 
          <span v-if="others()">
            <button class="btn btn-sm" v-show="followingState" @click="changeFollow"><i class="fas fa-user-check"></i> 팔로잉</button>
            <button class="btn btn-sm" v-show="!followingState" @click="changeFollow"><i class="fas fa-user-plus"></i> 팔로우</button>
          </span>
        </h2>
      </div>
      <div class="row justify-content-between setWidth mb-3">
        <!-- <p> -->
          <span>리뷰 수 {{userInfo.reviews.length }}</span>
          <span>팔로워 {{this.followers}}</span>
          <span>팔로우 {{this.followings}}</span>
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
import Swal from 'sweetalert2'



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
      followingState: false,
      followers: 0,
      followings: 0,
    }
    // followers: this.userInfo.followers.length,
    // followings: this.userInfo.followings.length
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
    },
    others() {
      console.log(this.userInfo.id, this.$cookies.userId)
      if (this.userInfo.id == this.$cookies.get('userId')){
        return false
      } else {
        return true
      }
    },
    changeFollow() {
      if (this.$cookies.get('auth-token')){
        const config = {
          headers: {
            'Authorization': `Token ${this.$cookies.get('auth-token')}`
          }
        }
        this.followingState = !this.followingState
        axios.get(SERVER.URL + '/accounts/' + this.$route.params.userId + '/follow/', config)
          .then( res => {
            console.log("RES",res)
            
            this.followers = res.data
            // this.followings =this.userInfo.followings.length
            })
          .catch( err => {
            console.log(err)
          })
      }else {
        const error = Swal.mixin({
              position: 'center',
              showConfirmButton: true,
              timer: 3000,
              timerProgressBar: false,
              })
        error.fire({
          icon: 'warning',
          title: "로그인이 필요합니다."
        })
      }
    },
    checkFollow() {
      // 여기 저녁먹고 다녀와서 작업하기 
      if (this.$cookies.get('auth-token')){
        axios.get(SERVER.URL + '/accounts/'+this.$route.params.userId +'/follow/'+this.$cookies.get('userId')+'/')
          .then(res =>{
            this.followingState = res.data
            console.log("checked Follow",res.data)
          })
          .catch(err => {
            console.log(err)
          })
      }
    }
  },
  created() {
    axios.get(SERVER.URL + '/accounts/'+this.$route.params.userId + '/info/')
    .then(res => {
      this.userInfo = res.data
      this.followers = this.userInfo.followers.length
      this.followings =this.userInfo.followings.length
      res.data.like.forEach( movie => {
        movie.poster_path=SERVER.IMAGEPATH.imagepath780 + movie.poster_path
      })
    })
    .catch(err => console.log(err))
    this.checkFollow()
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
  },
  beforeRouteLeave(to, from, next) {
    console.log('Leaving User Profile')
    next(false)
   
  },
  beforeRouteUdpate (to, from, next) {
    console.log("Reusing this component")
    this.userId = to.params.userId
    next(0)
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

p.nav-link{
  color: #345389;
  text-align:end;
  font-family: 'Do Hyeon' !important;
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

.nav-link:hover{
  cursor: pointer;
}

</style>