<template>
  <div>
    {{ userInfo }}
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
    getUserInfo() {
      const config = {
        headers : {
        'Authorization' : `Token ${this.$cookies.get('auth-token')}`
        },
      }
      axios.get(SERVER.URL + SERVER.getUserInfo,config )
        .then( res => this.userInfo = res.data)
    }
  },
  created() {
    this.getUserInfo()
  }
}
</script>

<style>

</style>