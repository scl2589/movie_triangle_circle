<template>
  <div>
    <h3 clsas="mb-3">좋아하는 영화를 골라주세요.</h3>
    <div class="row justify-content-between">
      <div v-for="movie in movies" :key="`movie_${movie.id}`">
          <!-- <img :src="posterURL + movie.poster_path" class="max-width"> -->
          <!-- 아래 부분 추가 -->
          <div @click="movieSelected(movie.id)" :id="`movie_${movie.id}`">
          <Card :data-image="posterURL + movie.poster_path">
            <h1 slot="header">{{ movie.title }}</h1>
            <p slot="content">{{ movie.overview | truncate(41, '...')}}</p>
          </Card>
          </div>
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
    movieSelected(movieId) {
      if (this.$cookies.get('auth-token')){
        const config = {
          headers: {
            'Authorization': `Token ${this.$cookies.get('auth-token')}`
          }
        }
      axios.get(SERVER.URL + "/movies/" + movieId +"/like/", config)
        .then( res => {
          if (res.data.liked === false) {
            let element = document.getElementById(`movie_${movieId}`);
            element.classList.add("liked");
          } else{
            let element = document.getElementById(`movie_${movieId}`);
            element.classList.remove("liked");
          }
          console.log(res.data)
        })
        .catch( err => console.log("NONO", err))
      }
    },
  },
  created(){
    this.fetchMovies()
  },
  filters: {
    truncate: function (text, length, suffix) {
            return text.substring(0, length) + suffix;
        },
  }
}
</script>

<style scoped>
.max-width {
  max-width: 100%
}

.liked {
  opacity: 0.35;
}
</style>