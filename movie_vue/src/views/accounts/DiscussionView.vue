<template>
  <div>
   
    <div class="row">
      <div class="col-2 list-group"> 
        <div class="list-group-itm" v-for=" genre in genres" :key="genre.key">
          <router-link class="links list-group-item" :to="{ name: 'Genre', params: { genre: genre.name, genreData:genre,pageNum:0 }}">{{ genre.name }}</router-link>
        </div>
      </div>
      <router-view class="col-10" />
     </div>
  </div>
</template>

<script>
import axios from 'axios'
import SERVER from '@/api/index.js'
export default {
  name: 'Discussions',
  data() {
    return {
      genres: [],

      pageNum: 0,
      pageSize: 10,
    }
  },
  methods: {
    getGenre() {
      axios.get(SERVER.URL + SERVER.ROUTES.genres)
        .then( res => this.genres = res.data)
        .catch( err => console.log(err.response.data))
    },
    
    // nextPage() {
    //   this.pageNum += 1;
    // },
    // prevPage() {
    //   this.pageNum -= 1;
    // }
  },
  created() {
    this.getGenre()
    // this.$router.push({ name: 'Genre', params: { genre: 'SF', genreData:this.genres[0], pageNum:0 }})
  },
  // computed: {
  //   pageCount() {
  //     let listLeng = this.reviews.length,
  //     listSize = this.pageSize,
  //     page = Math.floor(listLeng/listSize);

  //     if (listLeng % listSize > 0) page += 1;
  //     return page;
  //   },
  //   paginatedData() {
  //     if (this.reviews.length >= 1){
  //       const start = this.pageNum * this.pageSize,
  //       end = start + this.pageSize;
  //       return this.reviews.slice(start, end);
  //     } else {
  //       return 0
  //     }
  //   }
  // }
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

.links{
  color: #345389;
  padding: 2px;
  text-align: center;
}

.links:hover {
  color: pink;
  text-decoration: none;
}

.list-group-item {
  border-radius: 0;
}

.list-group {
  border-radius: 5px;
}

/* .giveBorder {
  border: 1px solid rgba(0,0,0,.125);
} */
</style>