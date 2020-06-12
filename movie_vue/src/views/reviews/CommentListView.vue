<template>
  <div>
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
  </div>
</template>


<script>

export default {
  name: 'CommentList',
  data() {
    return {
      commentData: {
        content: null,
      },
    }
  },
  props: {
    comments: Object,
  },
  methods: {
  
  },


}

</script>

<style>

</style>

