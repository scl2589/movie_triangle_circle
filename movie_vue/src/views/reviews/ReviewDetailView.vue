<template>
  <div class="container">
    <div class="card mb-3">
      <div class="card-header">
        <!-- 영화 제목 -->
        <p class="moviename link-hover" @click="goToMovieDetail">{{ review.movie_title }}</p>
        <!-- 제목 -->
        <h4 class="mb-0">{{ review.title }}
          <!-- 평점 -->
          <span class="rating" id="rating">
          </span>
        </h4>
        <!-- 게시글 정보 (작성자, 작성시간) -->
        <div class="row justify-content-between oneline pb-0">
          <small class="line-height">posted by <span class="link-hover" @click="goToUserPage(user.id)"><strong>{{ user.username }}</strong></span> on {{review.created_at}} <span style="font-weight:700">edited at</span> {{review.updated_at}}</small>
          <!-- 드롭다운 (삭제, 수정) -->
          <div v-if="reviewCreator" class="btn-group dropleft">
            <button type="button" class="btn btn-sm dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"></button>
            <div class="dropdown-menu">
              <p class="review-option give-highlight text-center" @click="deleteReview" >삭제</p>
              <p class="review-option give-highlight text-center" @click="updateReview" >수정</p>
            </div>
          </div>
        </div>
        
        
      </div>
      <!-- 리뷰 내용 -->
      <div class="card-body">
        <p class="card-text">{{ review.content}}</p>
      </div>

      <div class="card-footer text-muted">
        <!-- 댓글 목록 --> 
        <p>Comments</p>
          <hr>
          <div>
            <div v-for="comment in comments" :key="`comment_${comment.id}`">
              <div class="comments row justify-content-between">
                <!-- 댓글 작성자 -->
                <strong @click="goToUserPage(comment.user.id)">{{ comment.user.username}}</strong>
                <!-- 댓글 수정/삭제 드롭다운 -->
                <div v-if="commentCreator(comment.user.id)" class="btn-group dropleft comment-padding">
                  <button type="button" class="btn btn-sm dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"></button>
                  <div class="dropdown-menu">
                    <p class="border-bottom give-highlight text-center" @click="deleteComment(comment.id)" >삭제</p>
                    <p class="give-highlight text-center" @click="changeUpdateState(comment.id,comment.content)" >수정</p>
                  </div>
                </div>
              </div>
              <!-- 댓글 수정란 -->
              <div v-show="comment.id == currentComment.select" class="input-group mx-1 row">
                <textarea @keyup.enter="updateComment(comment.id, comment.content)" v-model="currentComment.content" type="content" class="col-xs-8 col-md-11" rows="5"></textarea>
                <button @click="updateComment(comment.id,comment.content)" class="input-group-append btn justify-content-center align-items-center col-xs-4 col-md-1 text-center">제출</button>
              </div>
              <p v-show="comment.id != currentComment.select">{{ comment.content }}</p>
              <small>{{ comment.created_at }}</small> 
              <hr>
            </div>
          </div>
        <!-- 댓글 생성 --> 
        <div class="input-group mx-1 row">
          <textarea v-model="commentData.content" class="col-xs-8 col-md-11" type="content" placeholder="댓글을 작성해주세요." rows="5" ></textarea>
          <button class="input-group-append btn justify-content-center align-items-center col-xs-4 col-md-1 text-center" @click="createComment">작성</button>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'
import Swal from 'sweetalert2'

export default {
  name: 'ReviewDetail',
  components: {
    // CommentList
  },
  data() {
    return {
      reviewData: [],
      review: [],
      commentData: {
        content: null,
      },
      currentComment: {
        select: null,
        content: null,
      },
      comments: [],
      user: [],
      reviewCreator: false,
      movieId: null,
      did_update: false,
    }
  },
  methods: {
    getReviewDetail() {
      axios.get(SERVER.URL + "/reviews/" + this.$route.params.reviewId  )
        .then( res => {
          this.review = res.data
          this.comments = this.review.comment_set
          this.user = res.data.user
          this.movieId = res.data.movie
          this.create_stars()
          console.log(String(this.user.id), this.$cookies.get('userId'))
          if (String(this.user.id)=== this.$cookies.get('userId')){
            this.reviewCreator = true;
          }
          else {
            this.reviewCreator = false;
          }
        })
        .catch( err => console.log(err))
    },
    create_stars() {
      let rating = document.getElementById("rating");
      let star = document.createElement("i")
      star.classList.add("fas", "fa-star")
      star.setAttribute("style", "color:#345389")
      for (let i = 0; i < this.review.rank; i++){
        let cln = star.cloneNode(true);
        rating.appendChild(cln);
      }
      let empty_star = document.createElement("i")
      empty_star.classList.add("far", "fa-star")
      for (let i = 0; i < 5 - this.review.rank ; i ++ ){
        let empty_cln = empty_star.cloneNode(true);
        rating.appendChild(empty_cln);
      }
    },
    createComment() {
      if ( this.$cookies.get('auth-token')) {
        const config = {
          headers : {
          'Authorization' : `Token ${this.$cookies.get('auth-token')}`
          },
        }
        axios.post(SERVER.URL + "/reviews/" + this.$route.params.reviewId + "/comment_create/",this.commentData,config)
          .then( () => {
            this.getComment()
            this.currentComment.content = this.commentData.content
            this.commentData.content = null
            
          })
          .catch( err => console.log(err) )  
        }
      
      },
    getComment() {
      axios.get(SERVER.URL + "/reviews/" + this.$route.params.reviewId + "/get_comments/")
        .then( res => this.comments = res.data)
        .catch( err => console.log(err) )
        
     },
    deleteReview() {
      if ( this.$cookies.get('auth-token')) {
        const config = {
          headers : {
          'Authorization' : `Token ${this.$cookies.get('auth-token')}`
          },
        }
        axios.delete(SERVER.URL + "/reviews/" + this.$route.params.reviewId, config)
          .then((res) => {
            if (res.data.success){
              this.$router.push({ name:'MovieDetail', params:{ movieId:this.review.movie }})
            }
            })
          .catch((err) => {
            console.log(err.response.data)
    
          })
        }
      },
    updateReview() {
      // console.log(String(this.user.id),this.$cookies.get('userId'))
      if ( this.$cookies.get('auth-token')) {
        if( String(this.user.id) === this.$cookies.get('userId')){ // 숫자와 문자열 같게
          this.reviewData = {
          title: this.review.title,
          content: this.review.content,
          rank: this.review.rank
        }
        this.$router.push({ name: 'ReviewCreate', params: {movieId:this.review.movie, reviewData:this.reviewData,reviewId: this.$route.params.reviewId}})
        }
      
      }
    },
    updateComment(comment_id) {
      if ( this.$cookies.get('auth-token')) {
        const config = {
          headers : {
          'Authorization' : `Token ${this.$cookies.get('auth-token')}`
          },
        }
        
        axios.put(SERVER.URL + "/reviews/update_comment/" + comment_id + "/" , this.currentComment,config)
          .then((res) => {
            this.currentComment.select = null
            this.getComment()
            this.did_update = true
            console.log(res.data.success)
            })
          .catch((err) => {
            console.log(err.response.data)
                      // 모달 띄우기 
            const swal = Swal.mixin({
              position: 'center',
              showConfirmButton: true,
              // title: this.errorMessages,
              
            })
            swal.fire({
              icon: 'error',
              title: "댓글을 작성해주세요.",
              confirmButtonText: '확인'
            })

          })
      }
    },
    deleteComment(comment_id) {
      if ( this.$cookies.get('auth-token')) {
        const config = {
          headers : {
          'Authorization' : `Token ${this.$cookies.get('auth-token')}`
          },
        }
        axios.delete(SERVER.URL + "/reviews/" + this.$route.params.reviewId + "/comment_delete/" + comment_id, config)
          
          .then(() => {
            this.getComment()
            })
          .catch((err) => {
            console.log(err.response.data)
            
          })
        }
    },
    changeUpdateState(comment_id, comment_content) {
      if (this.currentComment.select && this.currentComment.select === comment_id){
        this.currentComment.select = null
      }
      else {
        this.currentComment.content = comment_content
        this.currentComment.select = comment_id
      }
    },
    goToUserPage(user_id) {
      this.$router.push({ name:'Profile', params:{ userId: user_id}})
    },
    goToMovieDetail() {
      this.$router.push({ name:'MovieDetail', params:{ movieId: this.movieId}})
    },
    commentCreator(user_id) {
      console.log("커멘트 아이디", user_id, this.$cookies.get('userId'))
      if (String(user_id) === this.$cookies.get('userId')){
        return true
      } else {
        return false
      }
      
    }

  },
  created() {
    this.getReviewDetail()

    },
}


</script>

<style scoped>
.btn {
  background-color:#6f8dbf;
  outline: transparent;
  color: white;
  border: transparent;
}

.btn:hover{
  background-color: #345389;
  color: white;
}

.btn-xs{
  padding: 5px 10px; 
  font-size: 12px;
  border-radius: 5px;
}

.card {
  border: none;
}
.card-header {
  border: none;
  padding-bottom: 0px;
  background-color: white;
}


.card-text{
  white-space: pre-wrap;
  color: #1f3459;
}

.card-text::first-letter{
  color: #903;
  float: left;
  font-family: Georgia;
  font-size: 40px;
  line-height: 30px;
  padding-top: 4px;
  padding-right: 8px;
  padding-left: 3px;
}

.comment-padding {
  padding-right: 12px;
}

.comments {
  padding-left: 15px;
}


.give-highlight:hover {
  background-color: #a0bef0;
}

.line-height{
  line-height: 28px;
}

.link-hover:hover{
  cursor: pointer;
}

.moviename {
  text-decoration: underline;
  color: rgba(0,0,0,.35);
}

.oneline{
  padding: 12px;
}

.rating{
  /* background-color: #345389; */
  border-radius: 10px;
}

.show p{
  padding: 5px;
  margin-bottom: 0;
}

.txtbox{
  width: 100%;
}

.update{
  display: none;
}


::-webkit-resizer {
  display: none;
}




</style>
