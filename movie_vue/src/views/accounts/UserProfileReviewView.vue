<template>
  <div class="mt-3">
    <table class="table" v-if="userInfo.reviews[0]">
      <thead>
        <tr>
          <th scope="col">Movie Title</th>
          <th scope="col">Review Title</th>
          <th scope="col">User Rank</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="review in paginatedData" :key="`review_${review}`" >
          <th data-label="Movie Title" scope="row" @click="getReviewDetail(review.review_id)">{{ review.movie_title }}</th>
          <td data-label="Review Title" @click="getReviewDetail(review.review_id)"> {{ review.review_title }}</td>
          <td data-label="User Rank" @click="getReviewDetail(review.review_id)" id="star-rating">
            <i class="fas fa-star" style="color: #345389"></i> {{ review.movie_rank}}</td>
          <!-- 별점. -->
          <!-- {{ create_stars(review.movie_rank[0].rank)}} -->
          
        </tr>
      </tbody>
    </table>
    <div class="btn-cover" v-if="paginatedData">
      <button :disabled="pageNum === 0" @click="prevPage" class="page-btn">이전</button>
      <span class="page-count">{{ pageNum + 1 }} / {{ pageCount }} 페이지</span>
      <button :disabled="pageNum >= pageCount - 1" @click="nextPage" class="page-btn">다음</button>
    </div>
    <div v-else class="mt-5 text-center">
      <h3> 영화 리뷰를 작성해주세요. </h3>
    </div>
  </div>
  
</template>

<script>

export default {
  name: 'UserProfileReviewView',
  props: {
    'userInfo': {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      pageNum: 0,
      pageSize: 10,
    }
  },
  methods: {
    getReviewDetail(reviewId) {
        this.$router.push({name:'ReviewDetail', 'params': {reviewId: reviewId}})
    },
    create_stars(rank) {
      let outer = document.getElementById("star_rating");
      let star = document.createElement("i")
      star.classList.add("fas", "fa-star")
      console.log("rating 1", outer)
      star.setAttribute("style", "color:#345389")
      for (let i = 0; i < rank; i++){
        let cln = star.cloneNode(true);
        console.log("rating 2", outer)
        outer.appendChild("cln 1",cln);
      }
      let empty_star = document.createElement("i")
      empty_star.classList.add("far", "fa-star")
      for (let i = 0; i < 5 - rank ; i ++ ){
        let empty_cln = empty_star.cloneNode(true);
        outer.appendChild(empty_cln);
      }
    },
    nextPage() {
      this.pageNum += 1;
    },
    prevPage() {
      this.pageNum -= 1;
    }
  },
  computed: {
    pageCount() {
      let listLeng = this.userInfo.reviews.length,
      listSize = this.pageSize,
      page = Math.floor(listLeng/listSize);

      if (listLeng % listSize > 0) page += 1;
      return page;
    },
    paginatedData() {
      if (this.userInfo.reviews.length >= 1){
        const start = this.pageNum * this.pageSize,
        end = start + this.pageSize;
        return this.userInfo.reviews.slice(start, end);
      } else {
        return 0
      }
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

.btn-cover {
  margin-top: 1.5rem;
  text-align: center;
  clear: both;
}
.btn-cover .page-btn {
  width: 5rem;
  height: 2rem;
  letter-spacing: 0.5px;
}
.btn-cover .page-count {
  padding: 0 1rem;
}

button {
  background-color:#6f8dbf;
  outline: transparent;
  color: white;
  border: transparent;
  border-radius: 5px;
}

button:hover{
  background-color: #345389;
}
</style>