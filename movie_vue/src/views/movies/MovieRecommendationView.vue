<template>
  <div>
    <h3>영화를 골라주세요.</h3>
    <div class="row" v-for="movie in movies" :key="`movie_${movie.id}`">
      <div class="col-3">
        {{movie.title}}
      </div>
    </div>
    <div class="row">
      <div class="col-3 d-flex justify-content-start mb-5">
        <button class="btn btn-danger" :to="{ name:'MovieRecommendation' }">좋아하는 영화가 없어요</button>
      </div>
      <div class="offset-6 col-3 d-flex justify-content-end mb-5">
        <a :to="{ name:'MovieList' }"><button class="btn btn-danger">다 선택했어요</button></a>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'
export default {
  name: 'MovieRecommendation',
  data() {
    return {
      movies: []
    }
  },
  methods: {
    fetchMovies() {
      axios.get(SERVER.URL + SERVER.ROUTES.movieRecommendation)
        .then(res => {
          this.movies = res.data
        })
        .catch(err => console.error(err))
    }
  },
}
</script>

<style>

</style>