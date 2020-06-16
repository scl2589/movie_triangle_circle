<template>

<div v-if="userInfo.like" class="mb-5">
  <div v-for="likedMovie in paginatedData" :key="`like_${likedMovie.id}`" class="container" >
      <div class="content" @click="goToMovie(likedMovie.id)">
          <div class="content-overlay"></div>
          <img class="content-image" :src="likedMovie.poster_path">
          <div class="content-details fadeIn-top">
              <h3>{{ likedMovie.title}}</h3>
              <p><i class="fas fa-heart mr-2"></i>{{ likedMovie.like }}</p>
          </div>
      </div>
  </div>
  <div class="btn-cover" v-if="paginatedData">
    <button :disabled="pageNum===0" @click="prevPage" class="page-btn">이전</button>
    <span class="page-count">{{ pageNum + 1}} / {{ pageCount }} 페이지</span>
    <button :disabled="pageNum >= pageCount - 1" @click="nextPage" class="page-btn">다음</button>
  </div>
  <div v-else class="mt-5 text-center">
    <h3>좋아요를 누른 영화가 없습니다.</h3>
  </div>
</div>

</template>

<script>
// import Paginate from 'vuejs-paginate'

export default {
  name: 'UserProfileLikedView',
  props: {
    'userInfo': {
      type: Array,
      required: true
    }
  },
  data() {
    return {
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
    totalData() { 
      let length = this.userInfo.like.length 
      return Math.floor(length/9) + 1
    },
    pageCount() {
      let listLeng = this.userInfo.like.length,
      listSize = this.pageSize,
      page = Math.floor(listLeng/listSize);

      if (listLeng % listSize > 0) page += 1;
      return page;
    },
    paginatedData() {
      if (this.userInfo.like.length >= 1){
        const start = this.pageNum * this.pageSize,
        end = start + this.pageSize;
        return this.userInfo.like.slice(start, end);
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

.container{
  padding: 1em 0;
  float: left;
  width: 50%;
}
@media screen and (max-width: 640px){
  .container{
    display: block;
    width: 100%;
  }
}

@media screen and (min-width: 900px){
  .container{
    width: 33.33333%;
  }
}

.container .title{
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
  font-size: 1.5em;
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

.page-btn:hover {
  background-color: #345389;
  cursor: pointer;
}

</style>
