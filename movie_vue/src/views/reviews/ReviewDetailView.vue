<template>
  <div>
    <div class="card">
      <div class="card-header">
        <p class="mb-0">{{ review.title }}</p>
        <small>posted by <strong>{{ user.username }}</strong> on {{ review.created_at}}</small>
        <button @click="deleteReview" class="btn">삭제</button>
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
      review: [],
      commentData: {
        content: null,
      },
      comments: [],
      user: [],
    }
  },
  methods: {
    getReviewDetail() {
      axios.get(SERVER.URL + "/reviews/" + this.$route.params.reviewId  )
        .then( res => {
          this.review = res.data
          this.comments = this.review.comment_set
          this.user = res.data.user
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