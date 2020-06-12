export default {
    URL: 'http://localhost:8000',
    ROUTES: {
        signup: '/rest-auth/signup/',
        login: '/rest-auth/login/',
        logout: '/rest-auth/logout/',
        movieList: '/movies/',
        movieDetail: '/movies/:movieId/',
        createReview: '/reviews/create/',
        // articlesList: '/reviews/',
        // createComment: '/reviews/:articleId/comment_create/',
        revieweDetail: '/reviews/:reviewId/',
    }
}