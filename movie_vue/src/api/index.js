export default {
    URL: 'http://localhost:8000',
    ROUTES: {
        signup: '/rest-auth/signup/',
        login: '/rest-auth/login/',
        logout: '/rest-auth/logout/',
        movieList: '/movies/',
        movieDetail: '/movies/:movieId/',
        movieRecommendation: '/movies/user/recommendation/',
        createReview: '/reviews/create/',
        // articlesList: '/reviews/',
        // createComment: '/reviews/:articleId/comment_create/',
        revieweDetail: '/reviews/:reviewId/',
        getUserInfo: '/rest-auth/user/',
    }
}