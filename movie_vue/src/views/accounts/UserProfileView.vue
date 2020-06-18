<template>
  <div class="container">
    <div class="header mb-0 ">
      <div class="row justify-content-center mb-3">
        <h2> 
          {{ userInfo.username }} 
          <span v-if="others()">
            <button class="btn btn-sm" v-show="followingState" @click="changeFollow"><i class="fas fa-user-check"></i> 팔로잉</button>
            <button class="btn btn-sm" v-show="!followingState" @click="changeFollow"><i class="fas fa-user-plus"></i> 팔로우</button>
          </span>
        </h2>
      </div>
      <div class="row justify-content-center mb-3">
        <!-- <p> -->
          <span class="mr-5">리뷰 수 {{ userInfo.reviews.length }}</span>
          <span data-toggle="modal" data-target="#followers" class="make-hover mr-5">팔로워 {{ this.followers}}</span>
          <span data-toggle="modal" data-target="#followings" class="make-hover">팔로우 {{ this.followings}}</span>
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
   
  
  <!--follower Modal body 팔로워 모달 -->
  <div  class="modal follower-modal" tabindex="-1" role="dialog" id="followers">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">follower</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <h6>{{ userInfo.username }} 님을 팔로우하는 모든 사람이 여기에 표시됩니다.</h6>
          <hr>
          <div v-for="follower in userInfo.followersobj" :key="follower.id">
            <div class="row">
              <div class="pl-3 col-9">
                <span class=" pl-3 col-9 make-hover" @click="goToUserPage(follower.id)">{{ follower.username}}</span>
              </div>
              <div class="col-3 pr-3" v-if=" follower.id != authUserInfo.id">
                <button class="btn btn-sm " v-show="checkFollow2(follower,true)" @click="changeFollow"><i class="fas fa-user-check"></i> 팔로잉</button>
                <!-- check 그림이 팔로우가 되었다는 뜻 -->
                <button class=" btn btn-sm" v-show="!checkFollow2(follower, true)" @click="changeFollow"><i class="fas fa-user-plus"></i> 팔로우</button>
              </div>
              <hr>
            </div>
            
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- following modal body 팔로잉/팔로우 모달-->
  <div class="modal" tabindex="-1" role="dialog" id="followings">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">following</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <h6>{{ userInfo.username }}님이 팔로잉하는 모든 사람이 여기에 표시됩니다.</h6>
          <hr>
          <div v-for="following in userInfo.followingsobj" :key="following.id">
            <div class="row">
              <div class="pl-3 col-8 col-md-9">
                <span class=" pl-3 make-hover" @click="goToUserPage(following.id)">{{ following.username }}</span> 
              </div>
              <div class="col-4 col-md-3 pr-3" v-if=" following.id != authUserInfo.id">
                <button class="btn btn-sm " v-show="checkFollow2(following, false)" @click="changeFollow"><i class="fas fa-user-check"></i> 팔로잉</button>
                <button class=" btn btn-sm" v-show="!checkFollow2(following, false)" @click="changeFollow"><i class="fas fa-user-plus"></i> 팔로우</button>
              </div>
              <hr>
            </div>
            
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!--userInfo = id, username, like_movies, comment_set, review_set -->
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'
import UserProfileLiked from '@/views/accounts/UserProfileLikedView.vue'
import UserProfileReview from '@/views/accounts/UserProfileReviewView.vue'
import Swal from 'sweetalert2'
// import $ from 'jquery'


export default {
  name: 'UserProfile',
  
  data () {
    return {
      userInfo: [],
      authUserInfo: [],
      posterPaths: [],
      isLike: true,
      isReview: false,
      clickedLiked: true,
      clickedReview: false,
      followingState: false,
      followers: 0,
      followings: 0,
      error: null,
      post: null,
      state: true,
      check_person: "",
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
    },
    others() {
      // console.log(this.userInfo.id, this.$cookies.userId)
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
            console.log("changed Follow",res)
            
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
        return axios.get(SERVER.URL + '/accounts/'+this.$route.params.userId +'/follow/'+this.$cookies.get('userId')+'/')
          .then(res =>{
            this.followingState = res.data
            // console.log("checked Follow",res.data)
          })
          .catch(err => {
            console.log(err)
          })
      }
    },
   
    checkFollow2(user,flag) {
      console.log(this.authUserInfo.followingsobj)
      console.log(this.authUserInfo.followersobj)
      if (this.$cookies.get('auth-token') && flag){
          
          if ( this.authUserInfo.followings.includes(user.id)) {
            return true}
          else { return false}
      }
      else if (this.$cookies.get('auth-token') && !flag) {
        if ( this.authUserInfo.followings.includes(user.id)) {
            return true}
          else { return false}
      }
          
            // console.log("user.id", user.id, user.username, "this_id", this.$cookies.get('userId'), "res.data", res.data)
            // console.log(user.username)
            // console.log(res.data)
      

    },
    goToUserPage(user_id) {
      
      // 팔로워 모달 끄기 
      var modal = document.getElementById('followers')
      modal.classList.remove('show');
      modal.setAttribute('aria-hidden', 'true')
      modal.setAttribute('style', 'display:none')
      

      // 팔로잉 모달 끄기
      var modal2 = document.getElementById('followings')
      modal2.classList.remove('show');
      modal2.setAttribute('aria-hidden', 'true')
      modal2.setAttribute('style', 'display:none')
      

      // body에서 클래스 제거 
      var thisbody = document.body
      thisbody.classList.remove('modal-open')

      //  백드롭
      var modalBackdrops = document.getElementsByClassName('modal-backdrop')
      document.body.removeChild(modalBackdrops[0])

      // 라우터 이동
      this.$router.push({ name:'Profile', params:{ userId: user_id}})
      this.checkFollow()
    },

    
    getUserInfo(userId) {
      axios.get(SERVER.URL + '/accounts/'+ userId + '/info/')
    .then(res => {
      this.userInfo = res.data
      this.followers = this.userInfo.followers.length
      this.followings =this.userInfo.followings.length
      res.data.like.forEach( movie => {
        movie.poster_path=SERVER.IMAGEPATH.imagepath780 + movie.poster_path
      })
      axios.get(SERVER.URL + '/accounts/'+ this.$cookies.get('userId') + '/info/')
        .then( res => {
          this.authUserInfo = res.data
        })
        .catch( err => err.response.data)
      // console.log("SUCCESSFUL getUserInfo")
    })
    .catch(err => console.log( err))
    },
    // getUser(err, post){
    //   if (err) {
    //     this.error = err.toString()
    //   } else {
    //     this.post = post
    //   }
    // }
  },
  created() {
    this.getUserInfo(this.$route.params.userId)
    this.checkFollow()
  },
  beforeUpdate(){
    if(this.clickedLiked ===true){
      this.isLike = true
      this.isReview = false
    }
    if(this.clickedReview === true){
      this.isReview = true
      this.isLike = false
    } 
  },
  beforeRouteUpdate (to, from, next) {
    // console.log("Reusing this component")
    this.getUserInfo(to.params.userId)
    next();
  },
  // beforeRouteLeave(to, from, next) {
  //   this.checkFollow(check_person)
  // }
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

.make-hover{
  cursor: pointer;
}

</style>