<template>
<div class="container center mb-5 mt-3">
  <h3 class="d-flex justify-content-center" v-if="searchData.length != null">검색 결과: {{ searchData.length }} 건 </h3>
  <div>
    <div v-for="movie in paginatedData" :key="`movie_${movie.id}`" class="container2">
      <div class="content" @click="goToMovie(movie.id)">
        <div class="content-overlay"></div>
          <img class="content-image" :src="posterURL + movie.poster_path">
          <div class="content-details fadeIn-top">
              <h3>{{ movie.title}}</h3>
              <h5><i class="fas fa-heart mr-2"></i>{{ movie.like_user }}</h5>
          </div>
      </div>
    </div>
  </div>
  <div class="btn-cover" v-if="paginatedData">
    <button :disabled="pageNum===0" @click="prevPage" class="page-btn">이전</button>
    <span class="page-count">{{ pageNum + 1}} / {{ pageCount }} 페이지</span>
    <button :disabled="pageNum >= pageCount - 1" @click="nextPage" class="page-btn">다음</button>
  </div>
  <div v-else class="text-center">
    <h2 >검색 결과가 없습니다.</h2>
  </div>
</div>

</template>

<script>
// import axios from 'axios'
import SERVER from '@/api/index.js'
export default {
  name: 'Search',
  props: {
    searchData: { 
      type: Object,
      required: true 
    }
  },
  data() {
    return {
      posterURL: SERVER.IMAGEPATH.imagepath780,
      pageNum: 0,
      pageSize: 6,
    }
  },
  methods: {
    goToMovie(movie_pk){
      this.$router.push({
        name: 'MovieDetail',
        params: {movieId: movie_pk},
      })
    },
    nextPage() {
      this.pageNum += 1;
    },
    prevPage() {
      this.pageNum -= 1;
    }
  },
  computed: {
    pageCount() {
      let listLeng = this.searchData.length,
      listSize = this.pageSize,
      page = Math.floor(listLeng/listSize);

      if (listLeng % listSize > 0) page += 1;
      return page;
    },
    paginatedData() {
      if (this.searchData.length >= 1) {
        const start = this.pageNum * this.pageSize,
        end = start + this.pageSize;
        return this.searchData.slice(start, end);
      } else {
        return 0
      }
    }
 }
}
</script>
 
<style scoped>
@import url(https://fonts.googleapis.com/css?family=Raleway);

*, *:before, *:after{
  margin: 0;
  padding: 0;
  -webkit-box-sizing: border-box;
  -moz-box-sizing:border-box;
  box-sizing: border-box;
}

.main-title{
  color: #2d2d2d;
  text-align: center;
  text-transform: capitalize;
  padding: 0.7em 0;
}

.container2{
  padding: 1em 0;
  float: left;
  width: 50%;
}
@media screen and (max-width: 640px){
  .container2{
    display: block;
    width: 100%;
  }
}

@media screen and (min-width: 900px){
  .container2{
    width: 33.33333%;
  }
}

.container2 .title{
  color: #1a1a1a;
  text-align: center;
  margin-bottom: 10px;
}

.content {
  position: relative;
  width: 90%;
  max-width: 400px;
  margin: auto;
  overflow: hidden;
}

.content .content-overlay {
  background: rgba(0,0,0,0.7);
  position: absolute;
  height: 100%;
  width: 100%;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
  opacity: 0;
  -webkit-transition: all 0.4s ease-in-out 0s;
  -moz-transition: all 0.4s ease-in-out 0s;
  transition: all 0.4s ease-in-out 0s;
}

.content:hover .content-overlay{
  opacity: 1;
}

.content-image{
  width: 100%;
  height: 474px;
}

.content-details {
  position: absolute;
  text-align: center;
  padding-left: 1em;
  padding-right: 1em;
  width: 100%;
  top: 50%;
  left: 50%;
  opacity: 0;
  -webkit-transform: translate(-50%, -50%);
  -moz-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  -webkit-transition: all 0.3s ease-in-out 0s;
  -moz-transition: all 0.3s ease-in-out 0s;
  transition: all 0.3s ease-in-out 0s;
}

.content:hover .content-details{
  top: 50%;
  left: 50%;
  opacity: 1;
}

.content-details h3{
  color: #fff;
  font-weight: 500;
  letter-spacing: 0.15em;
  margin-bottom: 0.5em;
  text-transform: uppercase;
}

.content-details p{
  color: #fff;
  font-size: 0.8em;
}

.fadeIn-bottom{
  top: 80%;
}

.fadeIn-top{
  top: 20%;
}

.fadeIn-left{
  left: 20%;
}

.fadeIn-right{
  left: 80%;
}

.fa-heart{
  color: red;
}
/* .row{
  width: 100%;
} */

.center {
  margin: auto;
}


.btn-cover {
  margin-top: 1.5rem;
  text-align: center;
  clear: both;
}
.btn-cover .page-btn {
  width: 5rem;
  height: 2rem;
  letter-spacing: 0.5px;
}
.btn-cover .page-count {
  padding: 0 1rem;
}

button {
  background-color:#6f8dbf;
  outline: transparent;
  color: white;
  border: transparent;
  border-radius: 5px;
}

button:hover{
  background-color: #345389;
}

h5{
  color: white;

}

</style>