import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from '@/views/Home.vue'
import LoginView from '@/views/accounts/LoginView.vue'
import SignupView from '@/views/accounts/SignupView.vue'
import MovieListView from '@/views/movies/MovieListView.vue'
import MovieDetailView from '@/views/movies/MovieDetailView.vue'
import MovieRecommendationView from '@/views/movies/MovieRecommendationView.vue'
import ReviewCreateView from '@/views/reviews/ReviewCreateView.vue'
// import ListView from '@/views/areviews/ReviewListView.vue' 
import ReviewDetailView from '../views/reviews/ReviewDetailView.vue'
import UserProfileView from '@/views/accounts/UserProfileView.vue'

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
    path: '/accounts/:username',
    name: 'Profile',
    component: UserProfileView
  },
  {
    path: '/accounts/signup',
    name: 'Signup',
    component: SignupView
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
  // {
  //   path: '/reviews',
  //   name: 'List',
  //   component: ListView
  // },
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

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  const publicPages = ['Login', 'Signup', 'MovieList', 'MovieDetail', 'ReviewDetail']
  const authPages = ['Login', 'Signup', 'ReviewCreate', 'MovieRecommendation']
  const authRequired = !publicPages.includes(to.name)
  const unauthRequired = authPages.includes(to.name) // 로그인 해서는 안됨
  const isLoggedIn = Vue.$cookies.isKey('auth-token')

  if(unauthRequired && isLoggedIn) {
    next()
  }

  authRequired && !isLoggedIn ? next({ name: 'Login'}) : next()

})

export default router
