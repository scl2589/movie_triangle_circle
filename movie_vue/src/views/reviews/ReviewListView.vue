<template>
  <div>
    <table class="table mb-5" v-if="reviews">
      <thead>
        <tr>
          <!-- <th scope="col">#</th> -->
          <th scope="col">Title</th>
          <th scope="col">Username</th>
          <th scope="col">Rating</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="review in paginatedData" :key="`review_${review.id}`" @click="reviewDetail(review.id)" >
          <!-- <th data-label="ID" scope="row">{{ review.id }}</th> -->
          <td data-label="Title"> {{ review.title }}</td>
          <td data-label="Username">{{ review.user.username }}</td>
          <td data-label="Rating"><i class="fas fa-star" style="color: #345389"></i> {{ review.rank }}</td>
        </tr>
      </tbody>
    </table>
    <div class="btn-cover" v-if="paginatedData">
      <button :disabled="pageNum === 0" @click="prevPage" class="page-btn">이전</button>
      <span class="page-count">{{ pageNum + 1 }} / {{ pageCount }} 페이지</span>
      <button :disabled="pageNum >= pageCount - 1" @click="nextPage" class="page-btn">다음</button>
    </div>
    <div v-else class="mt-5 text-center">
      <h3> 리뷰를 작성해주세요! </h3>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReviewList',
  props: {
    reviews: {
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
    reviewDetail(reviewId) {
      this.$router.push({ name: 'ReviewDetail', params: { reviewId:reviewId }})
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
      let listLeng = this.reviews.length,
      listSize = this.pageSize,
      page = Math.floor(listLeng/listSize);

      if (listLeng % listSize > 0) page += 1;
      return page;
    },
    paginatedData() {
      if (this.reviews.length >= 1){
        const start = this.pageNum * this.pageSize,
        end = start + this.pageSize;
        return this.reviews.slice(start, end);
      } else {
        return 0
      }
    }
  }
}
</script>

<style scoped>

table {
  /* border: 1px solid #ccc; */
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
  /* border: 1px solid #ddd; */
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

.page-btn:hover {
  background-color: #345389;
  cursor: pointer;
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

th, td {
  font-family: 'Noto Sans KR';
  background-color: white;
}

table{
  border-style: none;
}

.table thead th {
  border-top-style: none;
  
}

</style>