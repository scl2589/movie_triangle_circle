<template>
  <div id="app" v-cloak>
    <ul class="navbar navbar-expand-lg nav nav-tabs d-lg-flex justify-content-between container d-none d-lg-block p-0" id="nav-tab" role="tablist">
      <div class="align-items-end row"> 
        <li class="nav-item" @click="goToMovieList" >
          <img src="./assets/logo.png" alt="세상의 모든 영화 로고" width="150px" title="세상의 모든 영화">
        </li>
        <li class="nav-item" role="presentation">
          <router-link class="nav-link"  :class="{active: isList }" :to="{ name:'MovieList' }">Movies</router-link>
        </li>
        <!-- <li class="nav-item" role="presentation">
          <router-link class="nav-link" :class="{active: isCreate}" v-if="isLoggedIn" :to="{ name:'Create' }">Create Review</router-link>
        </li> -->
        <li class="nav-item" role="presentation">
          <router-link class="nav-link" :class="{active: isDiscussions}" :to="{ name : 'Discussions'  }">Discussions</router-link>
        </li>
        <li class="nav-item" role="presentation">
          <router-link class="nav-link" :class="{active: isSignup}" v-if="!isLoggedIn" :to="{ name:'Signup' }">Signup</router-link>
        </li>
        <li class="nav-item" role="presentation">
          <router-link class="nav-link" :class="{active: isLogin}"  v-if="!isLoggedIn" :to="{ name:'Login' }">Login</router-link>
        </li>
        <li class="nav-item" role="presentation">
          <router-link class="nav-link" :class="{active: isProfile}" :key="$route.fullPath" v-if="isLoggedIn" :to="{ name:'Profile', params: { userId:this.$cookies.get('userId') } }">Profile</router-link>
          <!-- <button @click="clickedProfile" class="nav-link profile-button"  :class="{active: isProfile}" v-if="isLoggedIn"  type="submit">Profile</button> -->
        </li>
        <li class="nav-item" role="presentation">
          <router-link class="nav-link" v-if="isLoggedIn" @click.native="logout" to="/accounts/logout/">Logout</router-link>
        </li>
        
      </div>
      <div class="form-inline">
          <input @keyup.enter="search"  v-model="query" class="form-control mr-sm-2" placeholder="영화를 검색해주세요." aria-label="Search">
          <!-- <router-link :to="{name:'Search', params:{ query: query}}" @click.native="search" class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</router-link> -->
          <button @click="search" class="btn my-2 my-sm-0" type="submit">Search</button>
      </div>
    </ul>



    <!-- 모바일 버전 Navbar -->
    <nav class="navbar navbar-light mobile-background d-block d-lg-none ">
      <div class="d-flex justify-content-between">
        <img src="./assets/logo.png" class="navbar-brand" alt="세상의 모든 영화 로고"  title="세상의 모든 영화">
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
      </button>
      </div>
      

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item mr-auto" role="presentation">
            <router-link class="nav-link"  :class="{active: isList }" :to="{ name:'MovieList' }">Movies</router-link>
          </li>
          <!-- <li class="nav-item" role="presentation">
            <router-link class="nav-link" :class="{active: isCreate}" v-if="isLoggedIn" :to="{ name:'Create' }">Create Review</router-link>
          </li> -->
          <li class="nav-item mr-auto" role="presentation">
            <router-link class="nav-link" :class="{active: isDiscussions}" :to="{ name : 'Discussions'  }">Discussions</router-link>
          </li>
          <li class="nav-item mr-auto"  role="presentation">
            <router-link class="nav-link" :class="{active: isSignup}" v-if="!isLoggedIn" :to="{ name:'Signup' }">Signup</router-link>
          </li>
          <li class="nav-item mr-auto" role="presentation">
            <router-link class="nav-link" :class="{active: isLogin}"  v-if="!isLoggedIn" :to="{ name:'Login' }">Login</router-link>
          </li>
          <li class="nav-item mr-auto" role="presentation">
            <router-link class="nav-link" :class="{active: isProfile}" :key="$route.fullPath" v-if="isLoggedIn" :to="{ name:'Profile', params: { userId:this.$cookies.get('userId') } }">Profile</router-link>
            <!-- <button @click="clickedProfile" class="nav-link profile-button"  :class="{active: isProfile}" v-if="isLoggedIn"  type="submit">Profile</button> -->
          </li>
          <li class="nav-item mr-auto" role="presentation">
            <router-link class="nav-link" v-if="isLoggedIn" @click.native="logout" to="/accounts/logout/">Logout</router-link>
          </li>

        </ul>
        <div class="form-inline my-2 row p-2">
            <input @keyup.enter="search"  v-model="query" class="form-control col-8 mr-sm-2" placeholder="영화를 검색해주세요." aria-label="Search">
            <!-- <router-link :to="{name:'Search', params:{ query: query}}" @click.native="search" class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</router-link> -->
            <button @click="search" class="btn my-2 my-sm-0 col-4" type="submit">Search</button>
        </div>
      </div>
    </nav>



    <hr class="m-1  d-block d-lg-none ">
    <router-view class="mt-3 mb-5 container" @submit-login-data="login" @submit-signup-data="signup" :searchData="searchData" />
    <div class="m-5"></div>
    <div class="footer mt-5">
      <p class="footer-p">© 2020 Copyright: <i class="fab fa-github"></i> <a href="https://github.com/scl2589" target="_blank">chaelinshin96</a> | <i class="fab fa-github"></i><a href="https://github.com/ehtlfk" target="_blank"> ehtlfk</a></p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'
import Swal from 'sweetalert2'

export default {
  name: 'App',
  data () {
    return {
      isLoggedIn: false,
      errorMessages: "",
      isList: false,
      isSignup: false, 
      isLogin: false,
      isProfile: false,
      isDiscussions: false,
      query: null,
      searchData: [],
    }
  },
  methods: {
    setCookie(token){
      this.$cookies.set('auth-token', token)
      this.isLoggedIn = true
    },
    goToMovieList() {
      this.$router.push({name:'MovieList'})
    },
    // clickedLogo() {
    //   this.$router.go()
    // },
    signup(signupData){
      axios.post(SERVER.URL + SERVER.ROUTES.signup, signupData)
        .then( res => {
          this.setCookie(res.data.key)
          this.$cookies.set('userId', res.data.user.id)
          console.log(res.data)
          // this.$router.push({ name: 'MovieList' })
          // userId를 쿠키에 저장
          // axios.get(SERVER.URL +'/accounts/' + signupData.username+ '/')
          //   .then( res => {
          //   this.setCookie(res.data.key)
          //   this.$cookies.set('userId',res.data)
          //   })
          this.$router.push({name: 'MovieRecommendation'})
        })
        .catch( err => {
          console.log(err)
          if (signupData.password1.length < 8 || signupData.password2.length < 8 ){
            this.errorMessages = "비밀번호는 8자 이상이어야 합니다"
          }else if (signupData.password1 !== signupData.password2){
            this.errorMessages = "비밀번호가 일치하지 않습니다."
          }else {
            this.errorMessages = "해당 아이디가 이미 존재합니다."
          }            
          // 회원가입 에러 모달 띄우기
          const Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: false,
           })
           Toast.fire({
            icon: 'error',
            title: this.errorMessages
          })
        })

          
    },
    login(loginData) {
      axios.post(SERVER.URL + SERVER.ROUTES.login, loginData)
        .then( res => {
          this.setCookie(res.data.key)
          this.$cookies.set('userId',res.data.user.id)
          // this.setCookie('userId', res.data.user)
          // axios.get(SERVER.URL +'/accounts/' + loginData.username+ '/')
          //   .then( res => this.$cookies.set('userId',res.data))
          this.$router.push({ name: 'MovieList'})
          // 로그인 성공 모달 띄우기 
          const Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true,
            onOpen: (toast) => {
              toast.addEventListener('mouseenter', Swal.stopTimer)
              toast.addEventListener('mouseleave', Swal.resumeTimer)
              }
           })
           Toast.fire({
            icon: 'success',
            title: "로그인에 성공하였습니다."
          })

        })
        .catch( err => {
          console.log(err.response.data)
          // 로그인 실패 모달 띄우기
          if (loginData.password.length < 8 ){
            this.errorMessages = "비밀번호는 8자 이상이어야 합니다"
          }else {
            this.errorMessages = "로그인 정보를 다시 확인해주세요."
          }        
          const Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: false,
            onOpen: (toast) => {
              toast.addEventListener('mouseenter', Swal.stopTimer)
              toast.addEventListener('mouseleave', Swal.resumeTimer)
              }
           })
           Toast.fire({
            icon: 'error',
            title: this.errorMessages
          })
          })
    },
    logout() {
      const requestHeaders = {
        headers: {
          'Authorization': `Token ${this.$cookies.get('auth-token')}`
        }
      }
      
      axios.post(SERVER.URL + SERVER.ROUTES.logout,null, requestHeaders)
        .then( () => {
          axios.post(SERVER.URL + SERVER.ROUTES.createrecommend + this.$cookies.get('userId') + '/')
          this.$cookies.remove('auth-token')
          this.$cookies.remove('userId')
          this.isLoggedIn = false
          this.$router.push({ name: 'MovieList'})
          const Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true,
            onOpen: (toast) => {
              toast.addEventListener('mouseenter', Swal.stopTimer)
              toast.addEventListener('mouseleave', Swal.resumeTimer)
              }
           })
           Toast.fire({
            icon: 'success',
            title: '로그아웃되었습니다.'
          })
          
        })
        .catch( err => {
          console.log(err.response.data)
          this.errorMessages = "로그아웃을 실패하였습니다."
        })
    },
    search() {
      if (this.query){
        this.$router.push( {name: 'Search', params:{ query: this.query}})
        // :to="{name:'Search', params:{ query: query}}"
        const config = {
          params : {
            'query': this.query
          },
        }
        axios.get(SERVER.URL + SERVER.ROUTES.search, config)
          .then( (res) => {
            this.searchData = res.data
            this.query=""
          })
          .catch(err => {
            console.log(err.response.data)
            console.log("THIS IS SOMEHOW AN ERROR")
            })
      } else {
        const error = Swal.mixin({
          position: 'center',
          showConfirmButton: true,
          timer: 3000,
          timerProgressBar: false,
         })
        error.fire({
          icon: 'warning',
          title: "값을 입력해야 합니다."
        })
      }
      
    },
    clickedProfile() {
      this.$router.push({ name:'Profile', params: { userId:this.$cookies.get('userId') } })
      // this.$router.go()
    }
  },
  mounted() {
    this.isLoggedIn = this.$cookies.isKey('auth-token') ? true : false
    if(this.$route.name == 'MovieList'){
      this.isList = true
    } else if(this.$route.name == 'Signup'){
      this.isSignup = true
    } else if (this.$route.name == 'Login'){
      this.isLogin = true
    } else if (this.$route.name == 'Profile'){
      this.isProfile = true
    } else if (this.$route.name == 'Discussions'){
      this.isDiscussions = true
    }

  },
  updated(){
    if(this.$route.name == 'MovieList'){
      this.isList = true
    } else {
      this.isList = false
    }
    if(this.$route.name == 'Signup'){
      this.isSignup = true
    } else {
      this.isSignup = false
    }
    if(this.$route.name == 'Login'){
      this.isLogin = true
    } else {
      this.isLogin = false
    }
    if(this.$route.name == 'Profile'){
      this.isProfile = true
    } else{
      this.isProfile = false
    }
    if(this.$route.name == 'Discussions'){
      this.isDiscussions = true
    } else{
      this.isDiscussions = false
    }
  },
  
}

// Swal.fire({
//     title: 'Error!',
//     text: 'Do you want to continue',
//     icon: 'error',
//     confirmButtonText: 'Cool'
//   })

</script>


<style>
#app {
  font-family: 'Jua', Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #345389;
}

#nav {
  padding: 30px;
}


.nav-link{
  color: #345389;
  text-align:end;
  font-family: 'Gugi' !important;
}

.nav-link:hover{
  color: #345389
}
.nav-item > .active {
  /* color: #f5b893 !important;  */
  color: pink !important;
}

.btn {
  background-color:#6f8dbf;
  outline: transparent;
  color: white;
  border: transparent;
}

.btn:hover{
  background-color: #345389;
  color: white;
}

.footer{
  position: fixed;
  bottom: 0;
  background-color: #345389;
  color: white;  
  width: 100%;
  justify-content: center;
  display: flex;
  align-items: center;
}

.footer-p{
  line-height: 40px;
  margin: 0;
  font-family: 'Gugi';
}

.footer-p > a:link{
  color: white;
  text-decoration: none;
}


.footer-p  a:visited{
  text-decoration: none;
  color: white;
}

.footer-p a:hover {
  text-decoration: none;
  color: pink;
}

.m-5{
  clear: both;
  height: 20px;
}

.profile-button {
  background-color: white;
}
.nav-item {
  border-bottom: #345389;
}
.navbar-brand {
  max-width: 20%;
}

.mobile-background {
  background-color: white;
}

.navbar-light .navbar-nav .nav-link {
  color: #345389;
}

#app[v-cloak]{
  opacity: 0;
}
</style>

