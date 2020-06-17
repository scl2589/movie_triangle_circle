<template>
  <div>
    <h1>{{ genreData.name }}게시판 입니다</h1>
    
    <div class="input-group mx-1 row">
      <textarea v-model="g_commentData.content" class="col-xs-8 col-md-11" type="content" placeholder="글을 작성해주세요." rows="5" ></textarea>
      <button class="input-group-append btn justify-content-center align-items-center col-xs-4 col-md-1 text-center" @click="createGcomment(genreData.id)">작성</button>
    </div>
    <!-- <div v-for=" review in reveiwData" :key="review.id">
      {{ review }}
    </div> -->
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'

export default {
  name: 'Genre',
  data() {
    return {
      reviewData: [],
      g_commentData: {
        username: "",
        content: "",
      }
    }
  },
  props: {
    genreData: Object,
  },
  methods: {
    createGcomment(genre_id) {
      axios.post( SERVER.URL + `/movies/${genre_id}/gcomment/`,this.g_commentData)
        .then( res => {
          console.log(res.data)
          this.g_commentData.content = ""
        })
        .catch( res => console.log(res.response.data))
    },
    geteGcomment(genre_id) {
      axios.get( SERVER.URL + `/movies/${genre_id}/gcomment/`)
        .then( res => {
          this.reviewData = res.data
          // console.log(res.data)
        })
        .catch( res => console.log(res.response.data))
    },
  },
  created() {
    this.geteGcomment(this.genreData.id)
  }
}
</script>

<style>

</style>