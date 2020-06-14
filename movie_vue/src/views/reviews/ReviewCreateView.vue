<template>
  <div>
    <div class="form-group" >
      <input v-model="reviewData.title" type="text" id="title" placeholder="Title" class="inputs" autofocus>
    </div>
    <div>
      <input type="test">
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
      if (this.$route.params.reviewId) {
        axios.put(SERVER.URL + "/reviews/"+ this.$route.params.reviewId + "/update_review/", this.reviewData, config)
        .then(()=> {
          this.$router.push({ name: 'ReviewDetail', params: { "reviewId":this.$route.params.reviewId }})
        })
        .catch(err => console.log(err.response.data))
      }
      else {
        axios.post(SERVER.URL + "/movies/"+ this.$route.params.movieId + SERVER.ROUTES.createReview, this.reviewData, config)
        .then((res)=> {
          this.$router.push({ name: 'ReviewDetail', params: { "reviewId":res.data.id}})
        })
        .catch(err => console.log(err.response.data))
      }
    },

  },
  created() {
    if (this.$route.params.reviewData){
      this.reviewData = this.$route.params.reviewData
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