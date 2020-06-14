<template>
  <div>
    <div class="card">
      <div class="card-header">
        <p class="moviename">{{ review.movie }}</p>
        <h4 class="mb-0">{{ review.title }}</h4>
        <small @click="goToUserPage" class="username-hover">posted by <strong>{{ user.username }}</strong> on {{ review.created_at}}</small>
        <div v-if="reviewCreator">
          <button @click="deleteReview" class="btn">삭제</button>
        <button @click="updateReview" class="btn">수정</button>
        </div>
        
      </div>
      <div class="card-body">
        <p class="card-text">{{ review.content}}</p>
      </div>

      <div class="card-footer text-muted">
        <!-- 댓글 목록 --> 
        <p>Comments</p>
          <hr>
          <div>
            <div v-for="comment in comments" :key="`comment_${comment.id}`">
              <div>
                <strong @click="goToUserPage">{{ comment.user.username}}</strong>
                <div v-if="commentCreator(comment.user.id)">
                  <button @click="deleteComment(comment.id)" class="btn btn-sm">삭제</button>
                  <button @click="changeUpdateState(comment.id,comment.content)" class="btn btn-sm">수정</button>
                </div>
              </div>
              <div v-show="comment.id == currentComment.select">
                <textarea v-model="currentComment.content" type="content" placeholder="Content" class='txtbox' rows="5"></textarea>
                <button @click="updateComment(comment.id,comment.content)">제출</button>
              </div>
              <p v-show="comment.id != currentComment.select">{{ comment.content }}</p>
              <small>{{ comment.created_at }}</small> 
              <hr>
            </div>
          </div>
        <!-- 댓글 생성 --> 
        <div class="row mx-1">
          <textarea v-model="commentData.content" type="content" placeholder="Content" class='txtbox' rows="5"></textarea>
          <button class="btn offset-10 col-2 mt-2" @click="createComment">Submit</button>
        </div>

        
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'
// import CommentList from '@/views/reviews/CommentListView.vue'

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
      reviewCreator: false
    }
  },
  methods: {
    getReviewDetail() {
      axios.get(SERVER.URL + "/reviews/" + this.$route.params.reviewId  )
        .then( res => {
          this.review = res.data
          this.comments = this.review.comment_set
          this.user = res.data.user
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
            console.log(res.data)
             console.log(res.data.success)
            if ( res.data.success){
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
          content: this.review.content
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
            console.log(res.data.success)
            })
          .catch((err) => {
            console.log(err.response.data)
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
          
          .then((res) => {
            this.getComment()
            console.log(res.data)
            console.log(res.data.success)
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
    goToUserPage() {
      this.$router.push({ name:'Profile', params:{ userId: this.review.user.id}})
    },
    commentCreator(user_id) {
      console.log(user_id)
      if (user_id === this.$cookies.get('userId')){
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

<style>
.btn {
  background-color:#6f8dbf;
  outline: transparent;
  color: white;
  border: transparent;
}

.btn:hover{
  background-color: #345389;
}

.card-text{
  white-space: pre-wrap;
}

.update{
  display: none;
}

.username-hover:hover{
  cursor: pointer;
}
.card {
  border: none;
}
.card-header {
  border: none;
  border-bottom: 1px solid rgba(0,0,0,.125);
  background-color: white;
}
.moviename {
  text-decoration: underline;
  color: rgba(0,0,0,.35);
}
</style>
