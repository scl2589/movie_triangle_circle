<template>
<div class="container">
    <div class="header entire setbackground" v-bind:style="{'background-image': 'linear-gradient(to right, rgba(23, 37, 61, 1.00) 150px,rgba(52, 83, 137, 0.84) 100%), url(' + backDropURL + ')' }">
      <div class="inner-header p-3 d-flex float-this">
        <div class="row">
          <div class="col-md-4">
            <img :src="posterURL" class="setwidth justify-content-center" alt="영화포스터" >
          </div>
          <div class="col-md-8 p-4 justify-content-between" >
            <!-- :title="`${movie.release_date}`"  -->
            <h2><strong>{{ movie.title }}</strong><span class="dimcolor" :tooltip="`개봉일: ${movie.release_date}`" flow="right">({{date}})</span></h2>
            <!-- 장르 -->
            <h5><span v-for="genre in movie.genres" :key="`genre_${genre}`"><span href="#" class="badge mr-2 p-1 mb-1">{{ get_genre(genre)}}</span></span></h5>
            <div>
              <div class="c100 small" :class="computedClass" title="평점" data-toggle="tooltip" data-placement="top" >
                <span><strong>{{movie.vote_average*10}}</strong></span>
                <div class="slice" title="평점" >
                    <div class="bar" title="평점" ></div>
                    <div class="fill" title="평점" ></div>
                </div>
              </div>
              <!-- <span class="user_score mr-3">User<br>Score</span> -->
              
              <!-- 채워진 하트 -->
              <div class="d-inline-block heart-container ml-3">
                <i class="heart fas fa-heart fa-3x" v-show="like" @click="changeLike" style="color: tomato;" data-toggle="tooltip" data-placement="top">
                <span>{{ this.liked_users }}</span>
              </i> 
              </div>
              
               <!-- 빈 하트 -->
              <div class="d-inline-block heart-container">
                <i class="heart far fa-heart fa-3x" v-show="!like" @click="changeLike" style="color: white;" data-toggle="tooltip" data-placement="top">
                  <span>{{ this.liked_users }}</span>
                </i>
              </div>


              <button @click="showAlert()" class="btn button-transparent bg-transparent text-white pb-4 to-trailer" data-toggle="modal" :data-target="'#movie'+movie.movieId" role="dialog">► 예고편 보기 </button>
              
              <div v-if="video" class="modal fade" :id="'movie'+movie.movieId" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <MovieDetailTrailer :video="video"/>
              </div>
            </div>


            <!--줄거리 -->

            <div class="clear-float mt-3">
              <h4 class="text-left">줄거리</h4>
            </div>
            <div class="overview">
              <p >{{ movie.overview }}</p>
            </div>
            <div> 
              <!--감독 및 출연 배우 -->
              <p>{{ movie.director ? "감독: " + movie.director.replace(/,/g,'') : "" }}</p>
              <p>{{ movie.actor ? "배우: " + movie.actor.replace(/,/g,' ∙ ').slice(0,movie.actor.replace(/,/g,' ∙ ').length-2) : "" }}</p>
            </div>
          </div>
        </div>
     </div>
    </div>
    <div class="d-flex my-3 justify-content-between">
      <h3 class="vertical-align m-0">Reviews</h3>
      <button @click="GoToReviewClick" class="btn btn-sm ">리뷰 쓰러가기</button>
    </div>
    <div v-if="reviews.length" class="mt-3">
      <ReviewList :reviews="reviews"/>
    </div>
    <div v-else class="mb-5">
      <h5>리뷰를 작성해주세요!</h5>
    </div>
  </div>

</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'
import ReviewList from '@/views/reviews/ReviewListView.vue'
import MovieDetailTrailer from '@/views/movies/MovieDetailTrailerView.vue'
import Swal from 'sweetalert2'

// const API_KEY = process.env.VUE_APP_YOUTUBE_API_KEY;
// VUE_APP_YOUTUBE_API_KEY="AIzaSyCnCmWpk7t_J-utpA3f7TGDaq3PoON9jFM"
const API_KEY= process.env.VUE_APP_YOUTUBE_API_KEY;
const API_URL="https://www.googleapis.com/youtube/v3/search";


export default {
  name: 'MovieDetail',
  components: {
    ReviewList,
    MovieDetailTrailer,
  },
  data() {
    return {
      movie: "",
      movieId: this.$route.params.movieId,
      posterURL: "",
      backDropURL: "",
      reviews: [],
      video: "",
      videoUrl: "",
      like: false,
      genres: [],
      date: "",
      must_show: false,
      toast: "",
      liked_users :"", 
      //리뷰는 하나만
    }
  },
  computed: {
    computedClass() {
      let className = 'p' + this.movie.vote_average*10
      return className
    }
  },
  methods: {
    fetchMovie(){
      axios.get(SERVER.URL + "/movies/" + this.$route.params.movieId)
        .then(res => {
          const imgURL = 'https://image.tmdb.org/t/p/w780'
          this.movie = res.data
          this.date = this.movie.release_date.slice(0,4)
          this.posterURL = imgURL + this.movie.poster_path
          this.backDropURL = imgURL + this.movie.backdrop_path
          this.liked_users = this.movie.like_users.length
          axios.get(API_URL, {
            params: {
              key: API_KEY,
              part: "snippet",
              type: "video",
              q: this.movie.original_title +" official trailer",
              maxResults: 1,
            }
          })
          .then(res => {
            this.video = res.data.items[0]
          })
          .catch(err => {
            console.log(err)
            this.must_show = true
            // 유튜브 에러 모달 띄우기
            const Toast = Swal.mixin({
              position: 'center',
              showConfirmButton: true,
              timer: 3000,
              timerProgressBar: false,
              // customClass: 'title-class',
              width: '500px',
              })
              this.toast = Toast
            })
      })
      .catch(err => console.error(err))
    },
    showAlert() {
      if (this.must_show === true){
        this.toast.fire({
        icon: 'warning',
        title: "현재 예고편이 검색되지 않습니다.",
        
      })
      }
      
    },
    fetchReview() {
      axios.get(SERVER.URL+"/movies/"+this.$route.params.movieId+'/reviews/')
        .then( res => {
          this.reviews = res.data
        })
        .catch( err => console.error(err))
    },
    checkLike() {
      if (this.$cookies.get('auth-token')){
        axios.get(SERVER.URL + "/movies/" + this.$route.params.movieId +"/" + this.$cookies.get('userId') + "/like/" )
          .then( res => {
            this.like = res.data
            console.log(res.data)
          })
      }
    },

    changeLike() {
      if (this.$cookies.get('auth-token')){
        const config = {
          headers: {
            'Authorization': `Token ${this.$cookies.get('auth-token')}`
          }
        }
        this.like = !this.like
        axios.get(SERVER.URL + "/movies/" + this.$route.params.movieId +"/like/",config) // get은 body가 없다.
          .then( res => {
            console.log(res)
            this.liked_users = res.data.count
            })
          .catch( err => {
            console.log(err)
          })
      } else {
        const error = Swal.mixin({
              position: 'center',
              showConfirmButton: true,
              timer: 3000,
              timerProgressBar: false,
              
              })
        error.fire({
          icon: 'warning',
          title: "로그인이 필요합니다."
        })
      }
    },
    GoToReviewClick() {
   //rank_user ====id
    if (this.movie.rank_users.filter( rankobj =>
        rankobj == this.$cookies.get('userId')  // 이게 왜 false야, 참조
        ).length){
          const swal = Swal.mixin({
            position: 'center',
            showConfirmButton: true,
            // title: this.errorMessages,
            
            
          })
          swal.fire({
            icon: 'error',
            title: "이미 작성한 리뷰가 존재합니다.",
            confirmButtonText: '확인',
          })
      }
    else {
      this.$router.push({ name: 'ReviewCreate'})
    }
    },
    get_genre(genre_id) {
      const genre_dict = {12: '모험',
        14: '판타지',
        16: '애니메이션',
        18: '드라마',
        27: '공포',
        28: '액션',
        35: '코미디',
        36: '역사',
        37: '서부',
        53: '스릴러',
        80: '범죄',
        99: '다큐멘터리',
        878: 'SF',
        9648: '미스터리',
        10402: '음악',
        10749: '로맨스',
        10751: '가족',
        10752: '전쟁',
        10770: 'TV 영화'}
      return genre_dict[genre_id]
    }
  },
  created() {
    // 
    this.fetchMovie()
    this.fetchReview()
    if (this.$cookies.get('auth-token')){
      this.checkLike()
    
    }
  },
  
}
</script>

<style scoped>
.setwidth{
  max-width: 100%;
  /* margin: 20px; */
}

.setbackground{
  background-repeat: no-repeat;
  background-size: cover;
  z-index: 3;
  /* padding: 10px; */
  /* opacity: 0.3; */
  color: white;
  /* margin: 10px;
  margin-left: 0px; */
}
.dimcolor {
  color: #b2c6d4;
}

.clear-float{
  display:block;
  clear:both;
}

.to-trailer{
  background-color: transparent;
  border-color: transparent;
  box-shadow: none;
}


.vertical-align {
  line-height: 1.5;
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

.badge {
  background-color: #b3c6d5;
  color:#345389;
}

.overview {
  overflow: hidden;
  text-overflow: ellipsis;
  font-family: 'Noto Sans KR';
  font-size: smaller;
}

.heart{
  position: relative; 
}

.heart > span {
  position: absolute;
  width: 100%;
  z-index: 1;
  left: 0px;
  top: 0px;
  width: 5em;
  line-height: 5em;
  font-size: 0.2em;
  color: white; /* */
  display: block;
  text-align: center;
  white-space: nowrap;
}



[tooltip] {
  position: relative; /* opinion 1 */
}

/* START TOOLTIP STYLES */
[tooltip] {
  position: relative; /* opinion 1 */
}

/* Applies to all tooltips */
[tooltip]::before,
[tooltip]::after {
  text-transform: none; /* opinion 2 */
  font-size: .5em; /* opinion 3 */
  line-height: 1;
  user-select: none;
  pointer-events: none;
  position: absolute;
  display: none;
  opacity: 0;
}
[tooltip]::before {
  content: '';
  border: 5px solid transparent; /* opinion 4 */
  z-index: 1001; /* absurdity 1 */
}
[tooltip]::after {
  content: attr(tooltip); /* magic! */
  
  /* most of the rest of this is opinion */
  font-family:  'Noto Sans KR', Helvetica, sans-serif;
  text-align: center;
  
  /* 
    Let the content set the size of the tooltips 
    but this will also keep them from being obnoxious
    */
  min-width: 3em;
  max-width: 21em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding: 1ch 1.5ch;
  border-radius: .3ch;
  box-shadow: 0 1em 2em -.5em rgba(0, 0, 0, 0.35);
  background: #333;
  color: #fff;
  z-index: 1000; /* absurdity 2 */
}

/* Make the tooltips respond to hover */
[tooltip]:hover::before,
[tooltip]:hover::after {
  display: block;
}

/* don't show empty tooltips */
[tooltip='']::before,
[tooltip='']::after {
  display: none !important;
}



/* FLOW: RIGHT */
[tooltip][flow^="right"]::before {
  top: 50%;
  border-left-width: 0;
  border-right-color: #333;
  right: calc(0em - 5px);
  transform: translate(.5em, -50%);
}
[tooltip][flow^="right"]::after {
  top: 50%;
  left: calc(100% + 5px);
  transform: translate(.5em, -50%);
}

/* KEYFRAMES */
@keyframes tooltips-vert {
  to {
    opacity: .9;
    transform: translate(-50%, 0);
  }
}

@keyframes tooltips-horz {
  to {
    opacity: .9;
    transform: translate(0, -50%);
  }
}

/* FX All The Things */ 
[tooltip]:not([flow]):hover::before,
[tooltip]:not([flow]):hover::after,
[tooltip][flow^="up"]:hover::before,
[tooltip][flow^="up"]:hover::after,
[tooltip][flow^="down"]:hover::before,
[tooltip][flow^="down"]:hover::after {
  animation: tooltips-vert 300ms ease-out forwards;
}

[tooltip][flow^="left"]:hover::before,
[tooltip][flow^="left"]:hover::after,
[tooltip][flow^="right"]:hover::before,
[tooltip][flow^="right"]:hover::after {
  animation: tooltips-horz 300ms ease-out forwards;
}



/* .swal-wide{
  width:500px !important;
}

.swal2-title{
  font-size: 20px !important;
} */

.rect-auto,
.c100.p51 .slice,
.c100.p52 .slice,
.c100.p53 .slice,
.c100.p54 .slice,
.c100.p55 .slice,
.c100.p56 .slice,
.c100.p57 .slice,
.c100.p58 .slice,
.c100.p59 .slice,
.c100.p60 .slice,
.c100.p61 .slice,
.c100.p62 .slice,
.c100.p63 .slice,
.c100.p64 .slice,
.c100.p65 .slice,
.c100.p66 .slice,
.c100.p67 .slice,
.c100.p68 .slice,
.c100.p69 .slice,
.c100.p70 .slice,
.c100.p71 .slice,
.c100.p72 .slice,
.c100.p73 .slice,
.c100.p74 .slice,
.c100.p75 .slice,
.c100.p76 .slice,
.c100.p77 .slice,
.c100.p78 .slice,
.c100.p79 .slice,
.c100.p80 .slice,
.c100.p81 .slice,
.c100.p82 .slice,
.c100.p83 .slice,
.c100.p84 .slice,
.c100.p85 .slice,
.c100.p86 .slice,
.c100.p87 .slice,
.c100.p88 .slice,
.c100.p89 .slice,
.c100.p90 .slice,
.c100.p91 .slice,
.c100.p92 .slice,
.c100.p93 .slice,
.c100.p94 .slice,
.c100.p95 .slice,
.c100.p96 .slice,
.c100.p97 .slice,
.c100.p98 .slice,
.c100.p99 .slice,
.c100.p100 .slice {
  clip: rect(auto, auto, auto, auto);
}
.pie,
.c100 .bar,
.c100.p51 .fill,
.c100.p52 .fill,
.c100.p53 .fill,
.c100.p54 .fill,
.c100.p55 .fill,
.c100.p56 .fill,
.c100.p57 .fill,
.c100.p58 .fill,
.c100.p59 .fill,
.c100.p60 .fill,
.c100.p61 .fill,
.c100.p62 .fill,
.c100.p63 .fill,
.c100.p64 .fill,
.c100.p65 .fill,
.c100.p66 .fill,
.c100.p67 .fill,
.c100.p68 .fill,
.c100.p69 .fill,
.c100.p70 .fill,
.c100.p71 .fill,
.c100.p72 .fill,
.c100.p73 .fill,
.c100.p74 .fill,
.c100.p75 .fill,
.c100.p76 .fill,
.c100.p77 .fill,
.c100.p78 .fill,
.c100.p79 .fill,
.c100.p80 .fill,
.c100.p81 .fill,
.c100.p82 .fill,
.c100.p83 .fill,
.c100.p84 .fill,
.c100.p85 .fill,
.c100.p86 .fill,
.c100.p87 .fill,
.c100.p88 .fill,
.c100.p89 .fill,
.c100.p90 .fill,
.c100.p91 .fill,
.c100.p92 .fill,
.c100.p93 .fill,
.c100.p94 .fill,
.c100.p95 .fill,
.c100.p96 .fill,
.c100.p97 .fill,
.c100.p98 .fill,
.c100.p99 .fill,
.c100.p100 .fill {
  position: absolute;
  border: 0.08em solid #6f8dbf;
  width: 0.84em;
  height: 0.84em;
  clip: rect(0em, 0.5em, 1em, 0em);
  border-radius: 50%;
  -webkit-transform: rotate(0deg);
  -moz-transform: rotate(0deg);
  -ms-transform: rotate(0deg);
  -o-transform: rotate(0deg);
  transform: rotate(0deg);
}
.pie-fill,
.c100.p51 .bar:after,
.c100.p51 .fill,
.c100.p52 .bar:after,
.c100.p52 .fill,
.c100.p53 .bar:after,
.c100.p53 .fill,
.c100.p54 .bar:after,
.c100.p54 .fill,
.c100.p55 .bar:after,
.c100.p55 .fill,
.c100.p56 .bar:after,
.c100.p56 .fill,
.c100.p57 .bar:after,
.c100.p57 .fill,
.c100.p58 .bar:after,
.c100.p58 .fill,
.c100.p59 .bar:after,
.c100.p59 .fill,
.c100.p60 .bar:after,
.c100.p60 .fill,
.c100.p61 .bar:after,
.c100.p61 .fill,
.c100.p62 .bar:after,
.c100.p62 .fill,
.c100.p63 .bar:after,
.c100.p63 .fill,
.c100.p64 .bar:after,
.c100.p64 .fill,
.c100.p65 .bar:after,
.c100.p65 .fill,
.c100.p66 .bar:after,
.c100.p66 .fill,
.c100.p67 .bar:after,
.c100.p67 .fill,
.c100.p68 .bar:after,
.c100.p68 .fill,
.c100.p69 .bar:after,
.c100.p69 .fill,
.c100.p70 .bar:after,
.c100.p70 .fill,
.c100.p71 .bar:after,
.c100.p71 .fill,
.c100.p72 .bar:after,
.c100.p72 .fill,
.c100.p73 .bar:after,
.c100.p73 .fill,
.c100.p74 .bar:after,
.c100.p74 .fill,
.c100.p75 .bar:after,
.c100.p75 .fill,
.c100.p76 .bar:after,
.c100.p76 .fill,
.c100.p77 .bar:after,
.c100.p77 .fill,
.c100.p78 .bar:after,
.c100.p78 .fill,
.c100.p79 .bar:after,
.c100.p79 .fill,
.c100.p80 .bar:after,
.c100.p80 .fill,
.c100.p81 .bar:after,
.c100.p81 .fill,
.c100.p82 .bar:after,
.c100.p82 .fill,
.c100.p83 .bar:after,
.c100.p83 .fill,
.c100.p84 .bar:after,
.c100.p84 .fill,
.c100.p85 .bar:after,
.c100.p85 .fill,
.c100.p86 .bar:after,
.c100.p86 .fill,
.c100.p87 .bar:after,
.c100.p87 .fill,
.c100.p88 .bar:after,
.c100.p88 .fill,
.c100.p89 .bar:after,
.c100.p89 .fill,
.c100.p90 .bar:after,
.c100.p90 .fill,
.c100.p91 .bar:after,
.c100.p91 .fill,
.c100.p92 .bar:after,
.c100.p92 .fill,
.c100.p93 .bar:after,
.c100.p93 .fill,
.c100.p94 .bar:after,
.c100.p94 .fill,
.c100.p95 .bar:after,
.c100.p95 .fill,
.c100.p96 .bar:after,
.c100.p96 .fill,
.c100.p97 .bar:after,
.c100.p97 .fill,
.c100.p98 .bar:after,
.c100.p98 .fill,
.c100.p99 .bar:after,
.c100.p99 .fill,
.c100.p100 .bar:after,
.c100.p100 .fill {
  -webkit-transform: rotate(180deg);
  -moz-transform: rotate(180deg);
  -ms-transform: rotate(180deg);
  -o-transform: rotate(180deg);
  transform: rotate(180deg);
}
.c100 {
  position: relative;
  font-size: 120px;
  width: 1em;
  height: 1em;
  border-radius: 50%;
  float: left;
  margin: 0 0.1em 0.1em 0;
  background-color: white;
}
.c100 *,
.c100 *:before,
.c100 *:after {
  -webkit-box-sizing: content-box;
  -moz-box-sizing: content-box;
  box-sizing: content-box;
}
.c100.center {
  float: none;
  margin: 0 auto;
}
.c100.big {
  font-size: 240px;
}
.c100.small {
  font-size: 50px;
}
.c100 > span {
  position: absolute;
  width: 100%;
  z-index: 1;
  left: 0;
  top: 0;
  width: 5em;
  line-height: 5em;
  font-size: 0.2em;
  color: white; /* */
  display: block;
  text-align: center;
  white-space: nowrap;
  -webkit-transition-property: all;
  -moz-transition-property: all;
  -o-transition-property: all;
  transition-property: all;
  -webkit-transition-duration: 0.2s;
  -moz-transition-duration: 0.2s;
  -o-transition-duration: 0.2s;
  transition-duration: 0.2s;
  -webkit-transition-timing-function: ease-out;
  -moz-transition-timing-function: ease-out;
  -o-transition-timing-function: ease-out;
  transition-timing-function: ease-out;
}
.c100:after {
  position: absolute;
  top: 0.08em;
  left: 0.08em;
  display: block;
  content: " ";
  border-radius: 50%;
  background-color: black;
  width: 0.84em;
  height: 0.84em;
  -webkit-transition-property: all;
  -moz-transition-property: all;
  -o-transition-property: all;
  transition-property: all;
  -webkit-transition-duration: 0.2s;
  -moz-transition-duration: 0.2s;
  -o-transition-duration: 0.2s;
  transition-duration: 0.2s;
  -webkit-transition-timing-function: ease-in;
  -moz-transition-timing-function: ease-in;
  -o-transition-timing-function: ease-in;
  transition-timing-function: ease-in;
}
.c100 .slice {
  position: absolute;
  width: 1em;
  height: 1em;
  clip: rect(0em, 1em, 1em, 0.5em);
}
.c100.p1 .bar {
  -webkit-transform: rotate(3.6deg);
  -moz-transform: rotate(3.6deg);
  -ms-transform: rotate(3.6deg);
  -o-transform: rotate(3.6deg);
  transform: rotate(3.6deg);
}
.c100.p2 .bar {
  -webkit-transform: rotate(7.2deg);
  -moz-transform: rotate(7.2deg);
  -ms-transform: rotate(7.2deg);
  -o-transform: rotate(7.2deg);
  transform: rotate(7.2deg);
}
.c100.p3 .bar {
  -webkit-transform: rotate(10.8deg);
  -moz-transform: rotate(10.8deg);
  -ms-transform: rotate(10.8deg);
  -o-transform: rotate(10.8deg);
  transform: rotate(10.8deg);
}
.c100.p4 .bar {
  -webkit-transform: rotate(14.4deg);
  -moz-transform: rotate(14.4deg);
  -ms-transform: rotate(14.4deg);
  -o-transform: rotate(14.4deg);
  transform: rotate(14.4deg);
}
.c100.p5 .bar {
  -webkit-transform: rotate(18deg);
  -moz-transform: rotate(18deg);
  -ms-transform: rotate(18deg);
  -o-transform: rotate(18deg);
  transform: rotate(18deg);
}
.c100.p6 .bar {
  -webkit-transform: rotate(21.6deg);
  -moz-transform: rotate(21.6deg);
  -ms-transform: rotate(21.6deg);
  -o-transform: rotate(21.6deg);
  transform: rotate(21.6deg);
}
.c100.p7 .bar {
  -webkit-transform: rotate(25.2deg);
  -moz-transform: rotate(25.2deg);
  -ms-transform: rotate(25.2deg);
  -o-transform: rotate(25.2deg);
  transform: rotate(25.2deg);
}
.c100.p8 .bar {
  -webkit-transform: rotate(28.8deg);
  -moz-transform: rotate(28.8deg);
  -ms-transform: rotate(28.8deg);
  -o-transform: rotate(28.8deg);
  transform: rotate(28.8deg);
}
.c100.p9 .bar {
  -webkit-transform: rotate(32.4deg);
  -moz-transform: rotate(32.4deg);
  -ms-transform: rotate(32.4deg);
  -o-transform: rotate(32.4deg);
  transform: rotate(32.4deg);
}
.c100.p10 .bar {
  -webkit-transform: rotate(36deg);
  -moz-transform: rotate(36deg);
  -ms-transform: rotate(36deg);
  -o-transform: rotate(36deg);
  transform: rotate(36deg);
}
.c100.p11 .bar {
  -webkit-transform: rotate(39.6deg);
  -moz-transform: rotate(39.6deg);
  -ms-transform: rotate(39.6deg);
  -o-transform: rotate(39.6deg);
  transform: rotate(39.6deg);
}
.c100.p12 .bar {
  -webkit-transform: rotate(43.2deg);
  -moz-transform: rotate(43.2deg);
  -ms-transform: rotate(43.2deg);
  -o-transform: rotate(43.2deg);
  transform: rotate(43.2deg);
}
.c100.p13 .bar {
  -webkit-transform: rotate(46.800000000000004deg);
  -moz-transform: rotate(46.800000000000004deg);
  -ms-transform: rotate(46.800000000000004deg);
  -o-transform: rotate(46.800000000000004deg);
  transform: rotate(46.800000000000004deg);
}
.c100.p14 .bar {
  -webkit-transform: rotate(50.4deg);
  -moz-transform: rotate(50.4deg);
  -ms-transform: rotate(50.4deg);
  -o-transform: rotate(50.4deg);
  transform: rotate(50.4deg);
}
.c100.p15 .bar {
  -webkit-transform: rotate(54deg);
  -moz-transform: rotate(54deg);
  -ms-transform: rotate(54deg);
  -o-transform: rotate(54deg);
  transform: rotate(54deg);
}
.c100.p16 .bar {
  -webkit-transform: rotate(57.6deg);
  -moz-transform: rotate(57.6deg);
  -ms-transform: rotate(57.6deg);
  -o-transform: rotate(57.6deg);
  transform: rotate(57.6deg);
}
.c100.p17 .bar {
  -webkit-transform: rotate(61.2deg);
  -moz-transform: rotate(61.2deg);
  -ms-transform: rotate(61.2deg);
  -o-transform: rotate(61.2deg);
  transform: rotate(61.2deg);
}
.c100.p18 .bar {
  -webkit-transform: rotate(64.8deg);
  -moz-transform: rotate(64.8deg);
  -ms-transform: rotate(64.8deg);
  -o-transform: rotate(64.8deg);
  transform: rotate(64.8deg);
}
.c100.p19 .bar {
  -webkit-transform: rotate(68.4deg);
  -moz-transform: rotate(68.4deg);
  -ms-transform: rotate(68.4deg);
  -o-transform: rotate(68.4deg);
  transform: rotate(68.4deg);
}
.c100.p20 .bar {
  -webkit-transform: rotate(72deg);
  -moz-transform: rotate(72deg);
  -ms-transform: rotate(72deg);
  -o-transform: rotate(72deg);
  transform: rotate(72deg);
}
.c100.p21 .bar {
  -webkit-transform: rotate(75.60000000000001deg);
  -moz-transform: rotate(75.60000000000001deg);
  -ms-transform: rotate(75.60000000000001deg);
  -o-transform: rotate(75.60000000000001deg);
  transform: rotate(75.60000000000001deg);
}
.c100.p22 .bar {
  -webkit-transform: rotate(79.2deg);
  -moz-transform: rotate(79.2deg);
  -ms-transform: rotate(79.2deg);
  -o-transform: rotate(79.2deg);
  transform: rotate(79.2deg);
}
.c100.p23 .bar {
  -webkit-transform: rotate(82.8deg);
  -moz-transform: rotate(82.8deg);
  -ms-transform: rotate(82.8deg);
  -o-transform: rotate(82.8deg);
  transform: rotate(82.8deg);
}
.c100.p24 .bar {
  -webkit-transform: rotate(86.4deg);
  -moz-transform: rotate(86.4deg);
  -ms-transform: rotate(86.4deg);
  -o-transform: rotate(86.4deg);
  transform: rotate(86.4deg);
}
.c100.p25 .bar {
  -webkit-transform: rotate(90deg);
  -moz-transform: rotate(90deg);
  -ms-transform: rotate(90deg);
  -o-transform: rotate(90deg);
  transform: rotate(90deg);
}
.c100.p26 .bar {
  -webkit-transform: rotate(93.60000000000001deg);
  -moz-transform: rotate(93.60000000000001deg);
  -ms-transform: rotate(93.60000000000001deg);
  -o-transform: rotate(93.60000000000001deg);
  transform: rotate(93.60000000000001deg);
}
.c100.p27 .bar {
  -webkit-transform: rotate(97.2deg);
  -moz-transform: rotate(97.2deg);
  -ms-transform: rotate(97.2deg);
  -o-transform: rotate(97.2deg);
  transform: rotate(97.2deg);
}
.c100.p28 .bar {
  -webkit-transform: rotate(100.8deg);
  -moz-transform: rotate(100.8deg);
  -ms-transform: rotate(100.8deg);
  -o-transform: rotate(100.8deg);
  transform: rotate(100.8deg);
}
.c100.p29 .bar {
  -webkit-transform: rotate(104.4deg);
  -moz-transform: rotate(104.4deg);
  -ms-transform: rotate(104.4deg);
  -o-transform: rotate(104.4deg);
  transform: rotate(104.4deg);
}
.c100.p30 .bar {
  -webkit-transform: rotate(108deg);
  -moz-transform: rotate(108deg);
  -ms-transform: rotate(108deg);
  -o-transform: rotate(108deg);
  transform: rotate(108deg);
}
.c100.p31 .bar {
  -webkit-transform: rotate(111.60000000000001deg);
  -moz-transform: rotate(111.60000000000001deg);
  -ms-transform: rotate(111.60000000000001deg);
  -o-transform: rotate(111.60000000000001deg);
  transform: rotate(111.60000000000001deg);
}
.c100.p32 .bar {
  -webkit-transform: rotate(115.2deg);
  -moz-transform: rotate(115.2deg);
  -ms-transform: rotate(115.2deg);
  -o-transform: rotate(115.2deg);
  transform: rotate(115.2deg);
}
.c100.p33 .bar {
  -webkit-transform: rotate(118.8deg);
  -moz-transform: rotate(118.8deg);
  -ms-transform: rotate(118.8deg);
  -o-transform: rotate(118.8deg);
  transform: rotate(118.8deg);
}
.c100.p34 .bar {
  -webkit-transform: rotate(122.4deg);
  -moz-transform: rotate(122.4deg);
  -ms-transform: rotate(122.4deg);
  -o-transform: rotate(122.4deg);
  transform: rotate(122.4deg);
}
.c100.p35 .bar {
  -webkit-transform: rotate(126deg);
  -moz-transform: rotate(126deg);
  -ms-transform: rotate(126deg);
  -o-transform: rotate(126deg);
  transform: rotate(126deg);
}
.c100.p36 .bar {
  -webkit-transform: rotate(129.6deg);
  -moz-transform: rotate(129.6deg);
  -ms-transform: rotate(129.6deg);
  -o-transform: rotate(129.6deg);
  transform: rotate(129.6deg);
}
.c100.p37 .bar {
  -webkit-transform: rotate(133.20000000000002deg);
  -moz-transform: rotate(133.20000000000002deg);
  -ms-transform: rotate(133.20000000000002deg);
  -o-transform: rotate(133.20000000000002deg);
  transform: rotate(133.20000000000002deg);
}
.c100.p38 .bar {
  -webkit-transform: rotate(136.8deg);
  -moz-transform: rotate(136.8deg);
  -ms-transform: rotate(136.8deg);
  -o-transform: rotate(136.8deg);
  transform: rotate(136.8deg);
}
.c100.p39 .bar {
  -webkit-transform: rotate(140.4deg);
  -moz-transform: rotate(140.4deg);
  -ms-transform: rotate(140.4deg);
  -o-transform: rotate(140.4deg);
  transform: rotate(140.4deg);
}
.c100.p40 .bar {
  -webkit-transform: rotate(144deg);
  -moz-transform: rotate(144deg);
  -ms-transform: rotate(144deg);
  -o-transform: rotate(144deg);
  transform: rotate(144deg);
}
.c100.p41 .bar {
  -webkit-transform: rotate(147.6deg);
  -moz-transform: rotate(147.6deg);
  -ms-transform: rotate(147.6deg);
  -o-transform: rotate(147.6deg);
  transform: rotate(147.6deg);
}
.c100.p42 .bar {
  -webkit-transform: rotate(151.20000000000002deg);
  -moz-transform: rotate(151.20000000000002deg);
  -ms-transform: rotate(151.20000000000002deg);
  -o-transform: rotate(151.20000000000002deg);
  transform: rotate(151.20000000000002deg);
}
.c100.p43 .bar {
  -webkit-transform: rotate(154.8deg);
  -moz-transform: rotate(154.8deg);
  -ms-transform: rotate(154.8deg);
  -o-transform: rotate(154.8deg);
  transform: rotate(154.8deg);
}
.c100.p44 .bar {
  -webkit-transform: rotate(158.4deg);
  -moz-transform: rotate(158.4deg);
  -ms-transform: rotate(158.4deg);
  -o-transform: rotate(158.4deg);
  transform: rotate(158.4deg);
}
.c100.p45 .bar {
  -webkit-transform: rotate(162deg);
  -moz-transform: rotate(162deg);
  -ms-transform: rotate(162deg);
  -o-transform: rotate(162deg);
  transform: rotate(162deg);
}
.c100.p46 .bar {
  -webkit-transform: rotate(165.6deg);
  -moz-transform: rotate(165.6deg);
  -ms-transform: rotate(165.6deg);
  -o-transform: rotate(165.6deg);
  transform: rotate(165.6deg);
}
.c100.p47 .bar {
  -webkit-transform: rotate(169.20000000000002deg);
  -moz-transform: rotate(169.20000000000002deg);
  -ms-transform: rotate(169.20000000000002deg);
  -o-transform: rotate(169.20000000000002deg);
  transform: rotate(169.20000000000002deg);
}
.c100.p48 .bar {
  -webkit-transform: rotate(172.8deg);
  -moz-transform: rotate(172.8deg);
  -ms-transform: rotate(172.8deg);
  -o-transform: rotate(172.8deg);
  transform: rotate(172.8deg);
}
.c100.p49 .bar {
  -webkit-transform: rotate(176.4deg);
  -moz-transform: rotate(176.4deg);
  -ms-transform: rotate(176.4deg);
  -o-transform: rotate(176.4deg);
  transform: rotate(176.4deg);
}
.c100.p50 .bar {
  -webkit-transform: rotate(180deg);
  -moz-transform: rotate(180deg);
  -ms-transform: rotate(180deg);
  -o-transform: rotate(180deg);
  transform: rotate(180deg);
}
.c100.p51 .bar {
  -webkit-transform: rotate(183.6deg);
  -moz-transform: rotate(183.6deg);
  -ms-transform: rotate(183.6deg);
  -o-transform: rotate(183.6deg);
  transform: rotate(183.6deg);
}
.c100.p52 .bar {
  -webkit-transform: rotate(187.20000000000002deg);
  -moz-transform: rotate(187.20000000000002deg);
  -ms-transform: rotate(187.20000000000002deg);
  -o-transform: rotate(187.20000000000002deg);
  transform: rotate(187.20000000000002deg);
}
.c100.p53 .bar {
  -webkit-transform: rotate(190.8deg);
  -moz-transform: rotate(190.8deg);
  -ms-transform: rotate(190.8deg);
  -o-transform: rotate(190.8deg);
  transform: rotate(190.8deg);
}
.c100.p54 .bar {
  -webkit-transform: rotate(194.4deg);
  -moz-transform: rotate(194.4deg);
  -ms-transform: rotate(194.4deg);
  -o-transform: rotate(194.4deg);
  transform: rotate(194.4deg);
}
.c100.p55 .bar {
  -webkit-transform: rotate(198deg);
  -moz-transform: rotate(198deg);
  -ms-transform: rotate(198deg);
  -o-transform: rotate(198deg);
  transform: rotate(198deg);
}
.c100.p56 .bar {
  -webkit-transform: rotate(201.6deg);
  -moz-transform: rotate(201.6deg);
  -ms-transform: rotate(201.6deg);
  -o-transform: rotate(201.6deg);
  transform: rotate(201.6deg);
}
.c100.p57 .bar {
  -webkit-transform: rotate(205.20000000000002deg);
  -moz-transform: rotate(205.20000000000002deg);
  -ms-transform: rotate(205.20000000000002deg);
  -o-transform: rotate(205.20000000000002deg);
  transform: rotate(205.20000000000002deg);
}
.c100.p58 .bar {
  -webkit-transform: rotate(208.8deg);
  -moz-transform: rotate(208.8deg);
  -ms-transform: rotate(208.8deg);
  -o-transform: rotate(208.8deg);
  transform: rotate(208.8deg);
}
.c100.p59 .bar {
  -webkit-transform: rotate(212.4deg);
  -moz-transform: rotate(212.4deg);
  -ms-transform: rotate(212.4deg);
  -o-transform: rotate(212.4deg);
  transform: rotate(212.4deg);
}
.c100.p60 .bar {
  -webkit-transform: rotate(216deg);
  -moz-transform: rotate(216deg);
  -ms-transform: rotate(216deg);
  -o-transform: rotate(216deg);
  transform: rotate(216deg);
}
.c100.p61 .bar {
  -webkit-transform: rotate(219.6deg);
  -moz-transform: rotate(219.6deg);
  -ms-transform: rotate(219.6deg);
  -o-transform: rotate(219.6deg);
  transform: rotate(219.6deg);
}
.c100.p62 .bar {
  -webkit-transform: rotate(223.20000000000002deg);
  -moz-transform: rotate(223.20000000000002deg);
  -ms-transform: rotate(223.20000000000002deg);
  -o-transform: rotate(223.20000000000002deg);
  transform: rotate(223.20000000000002deg);
}
.c100.p63 .bar {
  -webkit-transform: rotate(226.8deg);
  -moz-transform: rotate(226.8deg);
  -ms-transform: rotate(226.8deg);
  -o-transform: rotate(226.8deg);
  transform: rotate(226.8deg);
}
.c100.p64 .bar {
  -webkit-transform: rotate(230.4deg);
  -moz-transform: rotate(230.4deg);
  -ms-transform: rotate(230.4deg);
  -o-transform: rotate(230.4deg);
  transform: rotate(230.4deg);
}
.c100.p65 .bar {
  -webkit-transform: rotate(234deg);
  -moz-transform: rotate(234deg);
  -ms-transform: rotate(234deg);
  -o-transform: rotate(234deg);
  transform: rotate(234deg);
}
.c100.p66 .bar {
  -webkit-transform: rotate(237.6deg);
  -moz-transform: rotate(237.6deg);
  -ms-transform: rotate(237.6deg);
  -o-transform: rotate(237.6deg);
  transform: rotate(237.6deg);
}
.c100.p67 .bar {
  -webkit-transform: rotate(241.20000000000002deg);
  -moz-transform: rotate(241.20000000000002deg);
  -ms-transform: rotate(241.20000000000002deg);
  -o-transform: rotate(241.20000000000002deg);
  transform: rotate(241.20000000000002deg);
}
.c100.p68 .bar {
  -webkit-transform: rotate(244.8deg);
  -moz-transform: rotate(244.8deg);
  -ms-transform: rotate(244.8deg);
  -o-transform: rotate(244.8deg);
  transform: rotate(244.8deg);
}
.c100.p69 .bar {
  -webkit-transform: rotate(248.4deg);
  -moz-transform: rotate(248.4deg);
  -ms-transform: rotate(248.4deg);
  -o-transform: rotate(248.4deg);
  transform: rotate(248.4deg);
}
.c100.p70 .bar {
  -webkit-transform: rotate(252deg);
  -moz-transform: rotate(252deg);
  -ms-transform: rotate(252deg);
  -o-transform: rotate(252deg);
  transform: rotate(252deg);
}
.c100.p71 .bar {
  -webkit-transform: rotate(255.6deg);
  -moz-transform: rotate(255.6deg);
  -ms-transform: rotate(255.6deg);
  -o-transform: rotate(255.6deg);
  transform: rotate(255.6deg);
}
.c100.p72 .bar {
  -webkit-transform: rotate(259.2deg);
  -moz-transform: rotate(259.2deg);
  -ms-transform: rotate(259.2deg);
  -o-transform: rotate(259.2deg);
  transform: rotate(259.2deg);
}
.c100.p73 .bar {
  -webkit-transform: rotate(262.8deg);
  -moz-transform: rotate(262.8deg);
  -ms-transform: rotate(262.8deg);
  -o-transform: rotate(262.8deg);
  transform: rotate(262.8deg);
}
.c100.p74 .bar {
  -webkit-transform: rotate(266.40000000000003deg);
  -moz-transform: rotate(266.40000000000003deg);
  -ms-transform: rotate(266.40000000000003deg);
  -o-transform: rotate(266.40000000000003deg);
  transform: rotate(266.40000000000003deg);
}
.c100.p75 .bar {
  -webkit-transform: rotate(270deg);
  -moz-transform: rotate(270deg);
  -ms-transform: rotate(270deg);
  -o-transform: rotate(270deg);
  transform: rotate(270deg);
}
.c100.p76 .bar {
  -webkit-transform: rotate(273.6deg);
  -moz-transform: rotate(273.6deg);
  -ms-transform: rotate(273.6deg);
  -o-transform: rotate(273.6deg);
  transform: rotate(273.6deg);
}
.c100.p77 .bar {
  -webkit-transform: rotate(277.2deg);
  -moz-transform: rotate(277.2deg);
  -ms-transform: rotate(277.2deg);
  -o-transform: rotate(277.2deg);
  transform: rotate(277.2deg);
}
.c100.p78 .bar {
  -webkit-transform: rotate(280.8deg);
  -moz-transform: rotate(280.8deg);
  -ms-transform: rotate(280.8deg);
  -o-transform: rotate(280.8deg);
  transform: rotate(280.8deg);
}
.c100.p79 .bar {
  -webkit-transform: rotate(284.40000000000003deg);
  -moz-transform: rotate(284.40000000000003deg);
  -ms-transform: rotate(284.40000000000003deg);
  -o-transform: rotate(284.40000000000003deg);
  transform: rotate(284.40000000000003deg);
}
.c100.p80 .bar {
  -webkit-transform: rotate(288deg);
  -moz-transform: rotate(288deg);
  -ms-transform: rotate(288deg);
  -o-transform: rotate(288deg);
  transform: rotate(288deg);
}
.c100.p81 .bar {
  -webkit-transform: rotate(291.6deg);
  -moz-transform: rotate(291.6deg);
  -ms-transform: rotate(291.6deg);
  -o-transform: rotate(291.6deg);
  transform: rotate(291.6deg);
}
.c100.p82 .bar {
  -webkit-transform: rotate(295.2deg);
  -moz-transform: rotate(295.2deg);
  -ms-transform: rotate(295.2deg);
  -o-transform: rotate(295.2deg);
  transform: rotate(295.2deg);
}
.c100.p83 .bar {
  -webkit-transform: rotate(298.8deg);
  -moz-transform: rotate(298.8deg);
  -ms-transform: rotate(298.8deg);
  -o-transform: rotate(298.8deg);
  transform: rotate(298.8deg);
}
.c100.p84 .bar {
  -webkit-transform: rotate(302.40000000000003deg);
  -moz-transform: rotate(302.40000000000003deg);
  -ms-transform: rotate(302.40000000000003deg);
  -o-transform: rotate(302.40000000000003deg);
  transform: rotate(302.40000000000003deg);
}
.c100.p85 .bar {
  -webkit-transform: rotate(306deg);
  -moz-transform: rotate(306deg);
  -ms-transform: rotate(306deg);
  -o-transform: rotate(306deg);
  transform: rotate(306deg);
}
.c100.p86 .bar {
  -webkit-transform: rotate(309.6deg);
  -moz-transform: rotate(309.6deg);
  -ms-transform: rotate(309.6deg);
  -o-transform: rotate(309.6deg);
  transform: rotate(309.6deg);
}
.c100.p87 .bar {
  -webkit-transform: rotate(313.2deg);
  -moz-transform: rotate(313.2deg);
  -ms-transform: rotate(313.2deg);
  -o-transform: rotate(313.2deg);
  transform: rotate(313.2deg);
}
.c100.p88 .bar {
  -webkit-transform: rotate(316.8deg);
  -moz-transform: rotate(316.8deg);
  -ms-transform: rotate(316.8deg);
  -o-transform: rotate(316.8deg);
  transform: rotate(316.8deg);
}
.c100.p89 .bar {
  -webkit-transform: rotate(320.40000000000003deg);
  -moz-transform: rotate(320.40000000000003deg);
  -ms-transform: rotate(320.40000000000003deg);
  -o-transform: rotate(320.40000000000003deg);
  transform: rotate(320.40000000000003deg);
}
.c100.p90 .bar {
  -webkit-transform: rotate(324deg);
  -moz-transform: rotate(324deg);
  -ms-transform: rotate(324deg);
  -o-transform: rotate(324deg);
  transform: rotate(324deg);
}
.c100.p91 .bar {
  -webkit-transform: rotate(327.6deg);
  -moz-transform: rotate(327.6deg);
  -ms-transform: rotate(327.6deg);
  -o-transform: rotate(327.6deg);
  transform: rotate(327.6deg);
}
.c100.p92 .bar {
  -webkit-transform: rotate(331.2deg);
  -moz-transform: rotate(331.2deg);
  -ms-transform: rotate(331.2deg);
  -o-transform: rotate(331.2deg);
  transform: rotate(331.2deg);
}
.c100.p93 .bar {
  -webkit-transform: rotate(334.8deg);
  -moz-transform: rotate(334.8deg);
  -ms-transform: rotate(334.8deg);
  -o-transform: rotate(334.8deg);
  transform: rotate(334.8deg);
}
.c100.p94 .bar {
  -webkit-transform: rotate(338.40000000000003deg);
  -moz-transform: rotate(338.40000000000003deg);
  -ms-transform: rotate(338.40000000000003deg);
  -o-transform: rotate(338.40000000000003deg);
  transform: rotate(338.40000000000003deg);
}
.c100.p95 .bar {
  -webkit-transform: rotate(342deg);
  -moz-transform: rotate(342deg);
  -ms-transform: rotate(342deg);
  -o-transform: rotate(342deg);
  transform: rotate(342deg);
}
.c100.p96 .bar {
  -webkit-transform: rotate(345.6deg);
  -moz-transform: rotate(345.6deg);
  -ms-transform: rotate(345.6deg);
  -o-transform: rotate(345.6deg);
  transform: rotate(345.6deg);
}
.c100.p97 .bar {
  -webkit-transform: rotate(349.2deg);
  -moz-transform: rotate(349.2deg);
  -ms-transform: rotate(349.2deg);
  -o-transform: rotate(349.2deg);
  transform: rotate(349.2deg);
}
.c100.p98 .bar {
  -webkit-transform: rotate(352.8deg);
  -moz-transform: rotate(352.8deg);
  -ms-transform: rotate(352.8deg);
  -o-transform: rotate(352.8deg);
  transform: rotate(352.8deg);
}
.c100.p99 .bar {
  -webkit-transform: rotate(356.40000000000003deg);
  -moz-transform: rotate(356.40000000000003deg);
  -ms-transform: rotate(356.40000000000003deg);
  -o-transform: rotate(356.40000000000003deg);
  transform: rotate(356.40000000000003deg);
}
.c100.p100 .bar {
  -webkit-transform: rotate(360deg);
  -moz-transform: rotate(360deg);
  -ms-transform: rotate(360deg);
  -o-transform: rotate(360deg);
  transform: rotate(360deg);
}
.c100:hover {
  cursor: default;
}
.c100:hover > span {
  width: 3.33em;
  line-height: 3.33em;
  font-size: 0.3em;
  color: #bf6f7e;
}
.c100:hover:after {
  top: 0.04em;
  left: 0.04em;
  width: 0.92em;
  height: 0.92em;
}



</style>

<style scoped lang="scss">


</style>