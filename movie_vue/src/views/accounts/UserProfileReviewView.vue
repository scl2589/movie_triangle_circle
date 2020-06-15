<template>
  <div v-if="userInfo.reviews">
    <!-- {{userInfo.reviews}} -->
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Movie Title</th>
          <th scope="col">Review Title</th>
          <th scope="col">User Rank</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="review in userInfo.reviews" :key="`review_${review}`" @click="reviewDetail(review.id)" >
          <th data-label="Movie Title" scope="row">{{ review.review_title }}</th>
          <td data-label="Review Title"> {{ review.movie_title }}</td>
          <td data-label="User Rank">{{ review.movie_rank[0]}}</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div v-else class="mt-5">
    <h3> 영화 리뷰를 작성해주세요. </h3>
  </div>
</template>

<script>
export default {
  name: 'UserProfileReviewView',
  props: {
    'userInfo': Object,
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