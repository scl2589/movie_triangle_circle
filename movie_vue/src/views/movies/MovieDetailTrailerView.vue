<template>
  <div v-if="video">
      <!-- Modal -->
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title text-dark m-0" id="exampleModalLabel" v-text="video.snippet.title"></h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="embed-responsive embed-responsive-16by9">
            <iframe class="embed-responsive-item" :src="videoUrl" allowfullscreen></iframe>
          </div>
          <hr>
          <div>
            <p v-text="video.snippet.publishedAt"></p>
            <p v-text="video.snippet.description"></p>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-info" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MovieDetailTrailer',
  props: {
    video: Object
  },
  computed: {
    videoUrl() {
      return `https://www.youtube.com/embed/${this.video.id.videoId}`;
    }
  }
}
</script>

<style scoped>
p{
  color: black;
}

</style>