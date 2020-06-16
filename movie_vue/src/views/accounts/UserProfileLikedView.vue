<template>

<div v-if="userInfo.like" class="mb-5">
  <div v-for="likedMovie in userInfo.like" :key="`like_${likedMovie.id}`" class="container" >
      <div class="content" @click="goToMovie(likedMovie.id)">
          <div class="content-overlay"></div>
          <img class="content-image" :src="likedMovie.poster_path">
          <div class="content-details fadeIn-top">
              <h3>{{ likedMovie.title}}</h3>
              <p><i class="fas fa-heart mr-2"></i>{{ likedMovie.like }}</p>
          </div>
      </div>
  </div>
  <div>
    <paginate
      class="pagination"
      v-model="page"
      :page-count="20"
      :page-range="5"
      :margin-pages="2"
      :click-handler="clickCallback"
      :prev-text="'Prev'"
      :next-text="'Next'"
      :container-class="'pagination'"
      :page-class="'page-item'">
    </paginate>

    <nav aria-label="Page navigation example">
  <ul class="pagination">
    <li class="page-item">
      <a class="page-link" href="#" aria-label="Previous">
        <span aria-hidden="true">&laquo;</span>
      </a>
    </li>
    <li class="page-item"><a class="page-link" href="#">1</a></li>
    <li class="page-item"><a class="page-link" href="#">2</a></li>
    <li class="page-item"><a class="page-link" href="#">3</a></li>
    <li class="page-item">
      <a class="page-link" href="#" aria-label="Next">
        <span aria-hidden="true">&raquo;</span>
      </a>
    </li>
  </ul>
</nav>
  </div>
  
</div>
<div v-else class="mt-5">
    <h3>마음에 드는 영화에 좋아요를 눌러주세요</h3>
</div>
</template>

<script>
export default {
  name: 'UserProfileLikedView',
  props: {
    'userInfo': Array, 
  },
  data() {
    return {
    }
  },
  methods: {
      goToMovie(movie_pk){
      this.$router.push({
        name: 'MovieDetail',
        params: {movieId: movie_pk},
      })
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
  height: 99%;
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

.pagination {
  clear: both;
  display: flex;
  justify-content: center;
  /* outline: black !important; */
}

</style>