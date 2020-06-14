<template>
  <div class="row">
    <div class="col-md-3">
      {{ userInfo }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserProfileLikedView',
  props: {
    'userInfo': Object, 
    'posterPaths': Object,
  },
}
</script>

<style>

</style>