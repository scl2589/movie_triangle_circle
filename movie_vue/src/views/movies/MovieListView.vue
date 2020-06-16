<template>
  <div class="container">
    <div v-if="this.$cookies.get('auth-token')" class="m-0">
      <h2 class="mt-3">Recommended Movies</h2>
      <div class="row scroll-sect recent-movies">
        <div class="row-inner">
            <div class="tile" v-for="movie in movies_recommend" :key="`movie_${movie.pk}`">
                <div class="tile-media">
                  <img :src="posterURL + movie.backdrop_path" @click="detail(movie.pk)">
                </div>
                <div class="text-center">
                  <p @click="detail(movie.pk)">{{ movie.title }}</p> 
                </div>
            </div>
        </div>
      </div>
    </div>

    <h2>Popular Now</h2>
    <div class="row scroll-sect recent-movies">
      <div class="row-inner">
          <div class="tile" v-for="movie in movies_popular" :key="`movie_${movie.pk}`">
              <div class="tile-media" >
                <img :src="posterURL + movie.backdrop_path" @click="detail(movie.pk)">
              </div>
              <div class="text-center">
                <p @click="detail(movie.pk)">{{ movie.title }}</p> 
              </div>
          </div>
      </div>
    </div>

    <h2>Recent Movies</h2>
    <div class="row scroll-sect recent-movies">
      <div class="row-inner">
          <div class="tile" v-for="movie in movies_recent" :key="`movie_${movie.pk}`">
              <div class="tile-media">
                <img :src="posterURL + movie.backdrop_path" @click="detail(movie.pk)">
              </div>
              <div class="text-center">
                <p @click="detail(movie.pk)">{{ movie.title }}</p> 
              </div>
          </div>
      </div>
    </div>
    
    

  </div>
  
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'

export default {
  name: 'MovieList',
  data() {
    return {
      posterURL: 'https://image.tmdb.org/t/p/w780/',
      movies_recent: [],
      movies_popular: [],
      movies_recommend: [],
    }
  },
  methods: {
    detail(movie_pk) {
      this.$router.push({
        name: 'MovieDetail',
        params: {movieId: movie_pk},
      })
    },
    fetchMovies() {
      let config = null
      if (this.$cookies.get('auth-token')) {
        config = {
          headers: {
            'Authorization': `Token ${this.$cookies.get('auth-token')}`
          }    
        }
      }
      axios.get(SERVER.URL + SERVER.ROUTES.movieList, config)
        .then(res => {
          this.movies_recent= res.data.slice(20, 40)
          this.movies_popular= res.data.slice(0, 20)
          if (res.data.length>40){
            this.movies_recommend = res.data.slice(40,60)
          }
        })
        .catch(err => console.error(err))
    }
  },
  created() {
    this.fetchMovies()
  },
}
</script>

<style scoped>
.row {
  overflow:scroll;
  width:100%;
}

.row-inner {
  white-space: nowrap;
  transition: 0.45s all;
  margin: 50px 10px;
}

.tile {
  position: relative;
  display:inline-block;
  margin: 0 5px;
  transition: 0.45s all;
  transform-origin: left center;
}

img {
  width:250px;
  height:150px;
  object-fit:cover;
  
}

.recent-movies {
  margin-bottom: 30px;
}
.row-inner:hover
{
  /*move to the left */
  transform: translateX(calc(250px*(-0.5)/2));
}

.row-inner:hover .tile {
  
  opacity: .3;
  
}

.row-inner:hover .tile:hover {
  /*set opacity back to 1 */
  transform: scale(1.5);
  opacity: 1;
  
}

.tile:hover ~ .tile {
  /* move tiles on the right to the right*/
  transform: translateX(calc(250px * 0.5));
}

.scroll-sect{
  overflow: hidden;
  
}
.scroll-sect::-webkit-scrollbar {
  width: 8px; height: 8px; border: 3px solid white; 
  } 
.scroll-sect::-webkit-scrollbar-button,.scroll-sect::-webkit-scrollbar-button:END {
  background-color: white;
}
.scroll-sect::-webkit-scrollbar-button:start:decrement{
}

.scroll-sect::-webkit-scrollbar-track {
  background: white; 
  -webkit-border-radius: 10px white; 
  border-radius:10px white;
  /* -webkit-box-shadow: inset 0 0 4px rgba(0,0,0,.2) */
  }

.scroll-sect::-webkit-scrollbar-thumb {
  height: 15px; 
  width: 50px; 
  background: #345389; 
  -webkit-border-radius: 15px; border-radius: 15px; 
  /* -webkit-box-shadow: inset 0 0 4px rgba(0,0,0,.1) */
  }

.scroll-sect:hover{
  overflow-x: scroll;
}
</style>
