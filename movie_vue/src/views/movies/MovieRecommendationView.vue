<template>
  <div>
    <h3>영화를 골라주세요.</h3>
    <div class="row justify-content-between">
      <div v-for="movie in movies" :key="`movie_${movie.id}`">
          <!-- <img :src="posterURL + movie.poster_path" class="max-width"> -->
          <!-- 아래 부분 추가 -->
          <Card :data-image="posterURL + movie.poster_path">
            <h1 slot="header">{{ movie.title }}</h1>
            <p slot="content">클릭해주세요.</p>
          </Card>
      </div>
    </div>
    <div class="row">
      <div class="col-3 d-flex justify-content-start mb-5">
        <button @click="no_movie" class="btn btn-danger" :to="{ name:'MovieRecommendation' }">좋아하는 영화가 없어요</button>
      </div>
      <div class="offset-6 col-3 d-flex justify-content-end mb-5">
        <button @click="done" class="btn btn-danger">다 선택했어요</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'
import Card from '@/views/movies/Card.vue'
export default {
  name: 'MovieRecommendation',
  data() {
    return {
      movies: [],
      posterURL: 'https://image.tmdb.org/t/p/w780/',
    }
  },
  props: ['dataImage'],
  components: {
    Card
  },
  methods: {
    fetchMovies() {
      axios.get(SERVER.URL + SERVER.ROUTES.movieRecommendation)
        .then(res => {
          this.movies = res.data
        })
        .catch(err => console.error(err))
    },
    done() {
      this.$router.push({name: 'MovieList'})
    },
    no_movie() {
      this.fetchMovies()
    },

  },
  created(){
    this.fetchMovies()
  },
}
</script>

<style>
.max-width {
  max-width: 100%
}
</style>