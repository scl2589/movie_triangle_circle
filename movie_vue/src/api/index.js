export default {
    URL: 'http://localhost:8000',
    ROUTES: {
        signup: '/rest-auth/signup/',
        login: '/rest-auth/login/',
        logout: '/rest-auth/logout/',
        profile: '/accounts/:userId/',
        movieList: '/movies/',
        movieDetail: '/movies/:movieId/',
        movieRecommendation: '/movies/user/recommendation/',
        createReview: '/reviews/create/',
        // articlesList: '/reviews/',
        // createComment: '/reviews/:articleId/comment_create/',
        reviewDetail: '/reviews/:reviewId/',
        // UserInfo: '/rest-auth/user/',
        userInfo: '/accounts/:userId/info',
        search: '/search/',
        recommendation: '/movies/getrecommend/',
    },
    IMAGEPATH: {
        imagepath780: 'https://image.tmdb.org/t/p/w780',
        
    }   
}