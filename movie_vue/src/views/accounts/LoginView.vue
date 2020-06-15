<template >
  <div class="container" >
    <h3>Login</h3>
    
      <div class="form-group" >
        <svg class="bi bi-person" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
          <path fill-rule="evenodd" d="M13 14s1 0 1-1-1-4-6-4-6 3-6 4 1 1 1 1h10zm-9.995-.944v-.002.002zM3.022 13h9.956a.274.274 0 0 0 .014-.002l.008-.002c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664a1.05 1.05 0 0 0 .022.004zm9.974.056v-.002.002zM8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm3-2a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
        </svg>
        <input v-model="loginData.username" id="username" class="inputs" type="text" placeholder="Username">
      </div>
      <div class="form-group">
        <svg class="bi bi-lock" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
          <path fill-rule="evenodd" d="M11.5 8h-7a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h7a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1zm-7-1a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h7a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-7zm0-3a3.5 3.5 0 1 1 7 0v3h-1V4a2.5 2.5 0 0 0-5 0v3h-1V4z"/>
        </svg>
        <input @keypress.enter="login" v-model="loginData.password" id="password" type="password" class="inputs" placeholder="Password" >
        
      </div>
      <div class="row mr-1">
        <button class="btn  offset-10 col-2" @click="login">Login</button>
      </div>
    
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      loginData: {
        username: null,
        password: null,
      }
    }
  },
  methods: {
    login() {
      this.$emit('submit-login-data', this.loginData)
    }
  }
}
</script>

<style scoped>
.inputs {
  border: none;
  border-radius: 0;
  border-bottom: 1px solid #757575;
  width: 100%;
}
.inputs:focus {
  outline: none;
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