<template>
  <div>

    <h3 class="text-center">{{ genreData.name }} 장르 게시판</h3>
    <table class="table  mb-5" v-if="genreData.genrereview_set.length">
      <thead>
        <tr>
          <th scope="col" style="width: 25%">익명아이디</th>
          <th scope="col" style="width: 75%">내용</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="review in paginatedData" :key="review.id">
          <td data-label="Username">{{ review.username }}</td>
          <td data-label="Content" class="content">{{ review.content }}</td>
        </tr>
      </tbody>
    </table>

    <div class="btn-cover mb-5" v-if="paginatedData">
      <button :disabled="pageNum === 0" @click="prevPage" class="page-btn">이전</button>
      <span class="page-count">{{ pageNum + 1 }} / {{ pageCount }} 페이지</span>
      <button :disabled="pageNum >= pageCount - 1" @click="nextPage" class="page-btn">다음</button>
    </div>

    <div v-else >
      <h5>글을 작성해주세요.</h5>
    </div>
    <div class="input-group mx-1 mt-3 row">
      <textarea v-model="g_commentData.content" class="col-xs-8 col-md-11" type="content" placeholder="글을 작성해주세요." rows="5" ></textarea>
      <button class="input-group-append btn justify-content-center align-items-center col-xs-4 col-md-1 text-center" @click="createGcomment(genreData.id)">작성</button>
    </div>
    
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'

export default {
  name: 'Genre',
  data() {
    return {
      reviewData: [],
      g_commentData: {
        username: "",
        content: "",
      },
      // pageNum: 0,
      pageSize: 10,
    }
  },
  props: {
    genreData: Object,
    pageNum: Number,
  },
  methods: {
    createGcomment(genre_id) {
      axios.post( SERVER.URL + `/movies/${genre_id}/gcomment/`,this.g_commentData)
        .then( res => {
          console.log(res.data)
          this.g_commentData.content = ""
          this.geteGcomment(genre_id)
        })
        .catch( res => console.log(res.response.data))
    },
    geteGcomment(genre_id) {
      axios.get( SERVER.URL + `/movies/${genre_id}/gcomment/`)
        .then( res => {
          this.genreData.genrereview_set = res.data.reverse()
        })
        .catch( res => console.log(res.response.data))
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
      let listLeng = this.genreData.genrereview_set.length,
      listSize = this.pageSize,
      page = Math.floor(listLeng/listSize);

      if (listLeng % listSize > 0) page += 1;
      return page;
    },
    paginatedData() {
      if (this.genreData.genrereview_set.length >= 1){
        const start = this.pageNum * this.pageSize,
        end = start + this.pageSize;
        return this.genreData.genrereview_set.slice(start, end);
      } else {
        return 0
      }
    }
  },
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

.content {
  white-space: pre-wrap;

}

</style>