<template>
  <div>
    <h1> HELLO </h1>
  </div>
</template>

<script>
// import axios from 'axios'
// import SERVER from '@/api/index.js'
export default {
  name: 'UserProfile',
  data () {
    return {
      userInfo: [],
    }
  },
  // 로그인 했을 때 자기 자신의 정보
  methods: {
    getUserInfo() {
      axios.get(SERVER.URL + SERVER.getUserInfo)
        .then( res => this.userInfo = res.data)
        .catch(err => console.log(err))
    }
  },
  created() {
    // this.getUserInfo()
  }
}
</script>

<style>

</style>