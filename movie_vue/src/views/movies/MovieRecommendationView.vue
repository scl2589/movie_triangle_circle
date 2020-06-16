<template>
  <div>
    <h2 class="mb-3 d-flex justify-content-center">좋아하는 영화를 골라주세요.</h2>
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
    <div class="row mt-3">
      <div class="col-3 d-flex justify-content-start mb-5">
        <button @click="no_movie" class="btn" :to="{ name:'MovieRecommendation' }">다른 영화도 보고싶어요</button>
      </div>
      <div class="offset-6 col-3 d-flex justify-content-end mb-5">
        <button @click="done" class="btn">다 선택했어요</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'
import Card from '@/views/movies/Card.vue'
import Swal from 'sweetalert2'
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
      // 여기에 권한을 주면 될듯
      const config = {
          headers: {
            'Authorization': `Token ${this.$cookies.get('auth-token')}`
          }
      }
      axios.get(SERVER.URL + SERVER.ROUTES.movieRecommendation,config)
        .then(res => {
          this.movies = res.data
        })
        .catch(err => console.error(err))
    },
    done() {  // 유저가 좋아하는 영화를 다 선택했을 경우 
      const config = {
        headers: {
          Authorization: `Token ${this.$cookies.get('auth-token')}`
        }
      }
      axios.get(SERVER.URL + SERVER.ROUTES.recommendation+ this.$cookies.get('userId')+"/", config)
        .then(() => {
          this.$router.push({name: 'MovieList'})
        })
      let timerInterval
      Swal.fire({
        title: '추천 영화를 생성중입니다.',
        html: '조금만 기다려주세요',
        timer: 5000,
        timerProgressBar: true,
        onBeforeOpen: () => {
          Swal.showLoading()
          timerInterval = setInterval(() => {
            const content = Swal.getContent()
            if (content) {
              const b = content.querySelector('b')
              if (b) {
                b.textContent = Swal.getTimerLeft()
              }
            }
          }, 100)
        },
        onClose: () => {
          clearInterval(timerInterval)
        }
      })
        .then((result) => {
          /* Read more about handling dismissals below */
          if (result.dismiss === Swal.DismissReason.timer) {
            console.log('I was closed by the timer')
          }
        })
      this.$router.push({name: 'Profile', params: {userId: this.$cookies.get('userId')} })

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