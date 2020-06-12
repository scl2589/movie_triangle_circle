<template>
  <div id="app" class="container">
    <ul class="nav nav-tabs d-flex align-items-end" id="nav-tab" role="tablist">
      <li class="nav-item" >
        <img src="./assets/logo.png" alt="세상의 모든 영화 로고" width="150px" title="세상의 모든 영화">
      </li>
      <li class="nav-item" role="presentation">
        <router-link class="nav-link" :class="{active: isList }" :to="{ name:'MovieList' }">Movies</router-link>
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
        <router-link class="nav-link" v-if="isLoggedIn" @click.native="logout" to="/accounts/logout/">Logout</router-link>
      </li>
    </ul>
    <div>
      {{ errorMessages}}
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
      // isCreate: false,
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
          this.$router.push({ name: 'MovieList' })
          // userId를 쿠키에 저장
          axios.get(SERVER.URL +'/accounts/' + signupData.username+ '/')
            .then( res => this.$cookies.set('userId',res.data))
        })
        .catch( err => console.log(err.response.data) )
    },
    login(loginData) {
      axios.post(SERVER.URL + SERVER.ROUTES.login, loginData)
        .then( res => {
          this.setCookie(res.data.key)
          axios.get(SERVER.URL +'/accounts/' + loginData.username+ '/')
            .then( res => this.$cookies.set('userId',res.data))
          this.$router.push({ name: 'MovieList'})

        })
        .catch( err => console.log(err.response.data))
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
          this.isLoggedIn = false
          this.$router.push({ name: 'MovieList'})
          this.$cookies.remove('userId')
        })
        .catch( err => console.log(err.response.data))
    },
  },
  mounted() {
    this.isLoggedIn = this.$cookies.isKey('auth-token') ? true : false
    if(this.$route.name == 'MovieList'){
      this.isList = true
    } else if(this.$route.name == 'Signup'){
      this.isSignup = true
    } else if (this.$route.name == 'Login'){
      this.isLogin = true
    } else if (this.$route.name == 'Create'){
      this.isCreate = true
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
    if(this.$route.name == 'Create'){
      this.isCreate = true
    } else{
      this.isCreate = false
    }

  }
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

a.nav-link{
  color: #345389;
  text-align:end;
}

.active {
  color: #f5b893 !important; 
}


</style>



