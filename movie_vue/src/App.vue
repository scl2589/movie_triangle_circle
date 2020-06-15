<template>
  <div id="app" class="container">
    <ul class="nav nav-tabs d-flex row justify-content-between" id="nav-tab" role="tablist">
      <div class="align-items-end row"> 
      <li class="nav-item" >
        <img src="./assets/logo.png" alt="세상의 모든 영화 로고" width="150px" title="세상의 모든 영화">
      </li>
      <li class="nav-item" role="presentation">
        <router-link class="nav-link"  :class="{active: isList }" :to="{ name:'MovieList' }">Movies</router-link>
      </li>
      <!-- <li class="nav-item" role="presentation">
        <router-link class="nav-link" :class="{active: isCreate}" v-if="isLoggedIn" :to="{ name:'Create' }">Create Review</router-link>
      </li> -->
      <li class="nav-item" role="presentation">
        <router-link class="nav-link" :class="{active: isSignup}" v-if="!isLoggedIn" :to="{ name:'Signup' }">Signup</router-link>
      </li>
      <li class="nav-item" role="presentation">
        <router-link class="nav-link" :class="{active: isLogin}"  v-if="!isLoggedIn" :to="{ name:'Login' }">Login</router-link>
      </li>
      <li class="nav-item" role="presentation">
        <router-link class="nav-link" :class="{active: isProfile}" v-if="isLoggedIn" :to="{ name:'Profile', params: { userId:this.$cookies.get('userId') } }">Profile</router-link>
      </li>
      <li class="nav-item" role="presentation">
        <router-link class="nav-link" v-if="isLoggedIn" @click.native="logout" to="/accounts/logout/">Logout</router-link>
      </li>
      </div>
      <div class="form-inline mx-2">
        <input v-model="query" class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
        <button @click="search" class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
      </div>
    </ul>
    <div id="errorMessageHere">
      <b-alert v-if="errorMessages" show fade dismissible>{{ errorMessages }}</b-alert>
    </div>
    <router-view class="mt-3" @submit-login-data="login" @submit-signup-data="signup" />
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'


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
      query: null
    }
  },
  methods: {
    setCookie(token){
      this.$cookies.set('auth-token', token)
      this.isLoggedIn = true
    },
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
          this.errorMessages = "회원가입 정보를 다시 확인해주세요."})
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
          

        })
        .catch( err => {
          console.log(err.response.data)
          this.errorMessages = "로그인 정보를 다시 확인해주세요."
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
          this.$cookies.remove('auth-token')
          this.$cookies.remove('userId')
          this.isLoggedIn = false
          this.$router.push({ name: 'MovieList'})
          
        })
        .catch( err => {
          console.log(err.response.data)
          this.errorMessages = "로그아웃을 실패하였습니다."
        })
    },
    showAlert() {
      setTimeout(() =>
        this.errorMessages = "", 2000);
    },
    search() {
      axios.get(SERVER.URL + SERVER.search,this.query)
        .then( () => {
          // console.log(res.data)
        })
        .catch( err => console.log(err.response.data))
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
  },
  
}
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #345389;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #345389;
}

#nav a.router-link-exact-active {
  color: #f5b893;
}

h3 {
  text-align: center;
}

.nav-link{
  color: #345389;
  text-align:end;
}

.active {
  color: #f5b893 !important; 
}


.btn {
  background-color:#6f8dbf;
  outline: transparent;
  color: white;
  border: transparent;
}

.btn:hover{
  background-color: #345389;
}


</style>



