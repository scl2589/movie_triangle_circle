<template>
  <div class="row justify-content-between">
      <div v-for="movie in searchData" :key="`movie_${movie.id}`">
          <!-- <img :src="posterURL + movie.poster_path" class="max-width"> -->
          <!-- 아래 부분 추가 -->
          <div @click="movieSelected(movie.id)" :id="`movie_${movie.id}`">
          <Card :data-image="posterURL + movie.poster_path">
            <h1 slot="header">{{ movie.title }}</h1>
          </Card>
          </div>
      </div>
    </div>
</template>

<script>
// import axios from 'axios'
import SERVER from '@/api/index.js'
import Card from '@/views/movies/Card.vue'
export default {
  name: 'Search',
  props: {
    searchData: Array,
  },
  data() {
    return {
      posterURL: SERVER.IMAGEPATH.imagepath780
    }
  },
  methods: {
    
  },
  components: {
    Card
  },

}
</script>

<style>

</style>