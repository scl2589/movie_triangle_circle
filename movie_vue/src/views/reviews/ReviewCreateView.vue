<template>
  <div>
    <div class="form-group" >
        <input v-model="reviewData.title" type="text" id="title" placeholder="Title" class="inputs" autofocus>
    </div>
    <div class="form-group">
        <textarea v-model="reviewData.content" type="content" id="content" 
        placeholder="Content" class='txtbox' rows="10">
        </textarea>
    </div>
    <div class="row mr-1">
      <button class="btn offset-10 col-2" @click="createReview">제출하기</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'
export default {
  name: 'ReviewCreate',
  data() {
    return {
      reviewData: {
        title: null,
        content: null,
      }
    }
  },
  methods: {
    createReview() {
      const config = {
        headers: {
          Authorization: `Token ${this.$cookies.get('auth-token')}`
        }
      }
      axios.post(SERVER.URL + "/movies/"+ this.$route.params.movieId + SERVER.ROUTES.createReview, this.reviewData, config)
        .then(()=> {
          this.$router.push({ name: 'MovieDetail', params: { "movieId":this.$route.params.movieId }})
        })
        .catch(err => console.log(err.response.data))
    },
    

  }
}
</script>

<style scoped>
.inputs {
  border: none;
  border-radius: 0;
  border-bottom: 1px solid #757575;
  width: 100%;
  padding: 0.5rem;
}
.inputs:focus {
  outline: none;
}
.txtbox{
  border-radius: 1;
  width: 100%;
  padding: 0.5rem;
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