<template>
  <div>
    <div class="card">
      <div class="card-header">
        <p class="mb-0">{{ review.title }}</p>
        <small>posted by <strong>{{ review.user.username }}</strong> on {{ review.created_at}}</small>
      </div>
      <div class="card-body">
        <p class="card-text">{{ review.content }}</p>
      </div>

      <div class="card-footer text-muted">
        <p>Comments</p>
          <hr>
          <div>
            <div v-for="comment in comments" :key="`comment_${comment.id}`">
              <p><strong>{{ comment.user.username}}</strong></p> 
              <p>{{ comment.content }}</p>
              <small>{{ comment.created_at }}</small>
              <hr>
            </div>
          </div>
        <div class="row mx-1">
          <textarea v-model="commentData.content" type="content" placeholder="Content" class='txtbox' rows="5"></textarea>
          <button class="btn btn-info offset-10 col-2 mt-2" @click="createComment">Submit</button>
        </div>
        <!-- 댓글 보여주는 란 -->
        <!-- <CommentList/> -->
        <!-- 댓글 작성란 -->
        
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'
import CommentList from '@/views/reviews/CommentListView.vue'

export default {
  name: 'ReviewDetail',
  components: {
    CommentList
  },
  data() {
    return {
      review: [],
      commentData: {
        content: null,
      },
      comments: [],
    }
  },
  methods: {
    getReviewDetail() {
      axios.get(SERVER.URL + "/reviews/" + this.$route.params.reviewId  )
        .then( res => {
          this.review = res.data
          this.comments = this.review.comment_set
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
          .catch( err => console.log(err) )
        
        axios.get( SERVER.URL + "/reviews/" +this.$route.params.reviewId +"/get_comments/")
          .then( res => this.comments = res.data )
          .catch( err => console.log(err))
          
        }
      // this.commentData.content = null
      }
    },
  created() {
    this.getReviewDetail()
  },
  computed: {
  
  }
}
</script>

<style>

</style>