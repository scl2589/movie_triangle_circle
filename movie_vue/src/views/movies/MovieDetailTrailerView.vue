<template>
  <div v-if="video">
      <!-- Modal -->
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title m-0" id="exampleModalLabel" v-text="video.snippet.title"></h5>
          <button type="button" class="btn"  @click="isClosed" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="embed-responsive embed-responsive-16by9 divScope">
            <iframe id="ytplayer" v-if="new_one" class="embed-responsive-item yt_player_iframe" :src="videoUrl" frameborder="0" allowfullscreen></iframe>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import $ from 'jquery'

// $('.stop-video').click(function(){
//     $('#youtube_player')[0].contentWindow.postMessage('{"event":"command","func":"' + 'stopVideo' + '","args":""}', '*');
// });


export default {
  name: 'MovieDetailTrailer',
  data() {
    return {
      // opened: true, 
      new_one: true,
    }
  },
  props: {
    video: Object,
    opened: Boolean,
  },
  computed: {
    videoUrl() {
      return `https://www.youtube.com/embed/${this.video.id.videoId}?enablejsapi=1&version=3&playerapiid=ytplayer`;
    },
    // isClosed() {
    //   return !this.new_one;
    // },
  },
  filters: {
    truncate: function (text, length, suffix) {
      if (text.length > length) {
          return text.substring(0, length) + suffix;
      } else {
          return text;
      }
    }
  },
  methods: {
    isClosed() {
      this.new_one = false
    },
  },
  updated() {
    this.new_one = true
  }

}




</script>

<style scoped>
p{
  color: black;
}
.video-description {
  white-space: pre-wrap;
}

.modal-title {
  color: white;
}

.modal-content {
  background-color: black;
}

.close {
  color: white;
}

</style>