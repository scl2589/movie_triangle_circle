<template>
  <div>
    <table class="table mb-5">
      <thead>
        <tr>
          <!-- <th scope="col">#</th> -->
          <th scope="col">Title</th>
          <th scope="col">Username</th>
          <th scope="col">Rating</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="review in reviews" :key="`review_${review.id}`" @click="reviewDetail(review.id)" >
          <!-- <th data-label="ID" scope="row">{{ review.id }}</th> -->
          <td data-label="Title"> {{ review.title }}</td>
          <td data-label="Username">{{ review.user.username }}</td>
          <td data-label="Rating"><i class="fas fa-star" style="color: #345389"></i> {{ review.rank }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'ReviewList',
  props: {
    reviews: Array,
  },
  methods: {
    reviewDetail(reviewId) {
      this.$router.push({ name: 'ReviewDetail', params: { reviewId:reviewId }})
    }
  }
}
</script>

<style scoped>

table {
  border: 1px solid #ccc;
  border-collapse: collapse;
  margin: 0;
  padding: 0;
  width: 100%;
  table-layout: fixed;
}

table caption {
  font-size: 1.5em;
  margin: .5em 0 .75em;
}

table tr {
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  padding: .35em;
}

table th,
table td {
  padding: .625em;
  text-align: center;
}

table th {
  font-size: .85em;
  letter-spacing: .1em;
  text-transform: uppercase;
}

@media screen and (max-width: 600px) {
  table {
    border: 0;
  }

  table caption {
    font-size: 1.3em;
  }
  
  table thead {
    border: none;
    clip: rect(0 0 0 0);
    height: 1px;
    margin: -1px;
    overflow: hidden;
    padding: 0;
    position: absolute;
    width: 1px;
  }
  
  table tr {
    border-bottom: 3px solid #ddd;
    display: block;
    margin-bottom: .625em;
  }
  
  table td {
    border-bottom: 1px solid #ddd;
    display: block;
    font-size: .8em;
    text-align: right;
  }
  
  table td::before {
    /*
    * aria-label has no advantage, it won't be read inside a table
    content: attr(aria-label);
    */
    content: attr(data-label);
    float: left;
    font-weight: bold;
    text-transform: uppercase;
  }
  
  table td:last-child {
    border-bottom: 0;
  }
}

</style>