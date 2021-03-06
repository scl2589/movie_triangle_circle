import Vue from 'vue'
import VueRouter from 'vue-router'

// User
import LoginView from '@/views/accounts/LoginView.vue'
import SignupView from '@/views/accounts/SignupView.vue'
import UserProfileView from '@/views/accounts/UserProfileView.vue'
import UserProfileLikedView from '@/views/accounts/UserProfileLikedView.vue'

//Movie
import MovieListView from '@/views/movies/MovieListView.vue'
import MovieDetailView from '@/views/movies/MovieDetailView.vue'
import MovieRecommendationView from '@/views/movies/MovieRecommendationView.vue'

// Review
import ReviewCreateView from '@/views/reviews/ReviewCreateView.vue'
import ReviewDetailView from '../views/reviews/ReviewDetailView.vue'

// Discussion
import DiscussionView from '@/views/accounts/DiscussionView.vue'
import Genre from '@/views/accounts/GenreView.vue'

// Search
import SearchView from '@/views/accounts/SearchView.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'MovieList',
    component: MovieListView
  },
  {
    path: '/accounts/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/accounts/:userId',
    name: 'Profile',
    component: UserProfileView,
    
  },
  {
    path: '/accounts/signup',
    name: 'Signup',
    component: SignupView
  },
  {
    path: '/search?query=:query',
    name: 'Search',
    component: SearchView,
    props: true
  },
  {
    path: '/movies/:movieId',
    name: 'MovieDetail',
    component: MovieDetailView,
  },
  {
    path: '/movies/:movieId/reviews/create',
    name: 'ReviewCreate',
    component: ReviewCreateView,
    props: true
  },
  {
    path: '/reviews/:reviewId',
    name: 'ReviewDetail',
    component: ReviewDetailView,

  },
  {
    path: '/movies/user/recommendation',
    name: 'MovieRecommendation',
    component: MovieRecommendationView,
  },
  {
    path: '/accounts/:userId/likedMovies',
    name: 'UserProfileLiked',
    component: UserProfileLikedView,
  },
  {
    path: '/discussions',
    children:[
        {
            path: ':genre',
            name: 'Genre',
            component: Genre,
            props: true
        }
    ],
    name: 'Discussions',
    component: DiscussionView
  },


]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  const publicPages = ['Login', 'Signup', 'MovieList', 'MovieDetail', 'ReviewDetail', 'Search', 'Discussions', 'Genre', 'Profile']
  const authPages = ['Login', 'Signup', 'ReviewCreate', 'MovieRecommendation', 'UserProfile']
  const authRequired = !publicPages.includes(to.name)
  const unauthRequired = authPages.includes(to.name) // 로그인 해서는 안됨
  const isLoggedIn = Vue.$cookies.isKey('auth-token')

  if(unauthRequired && isLoggedIn) {
    next()
  }

  authRequired && !isLoggedIn ? next({ name: 'Login'}) : next()
  
})


export default router
