from django.urls import path
from api import views

urlpatterns = [
    path('createUser/', views.NewUser.as_view()),
    path('login/', views.login),
    path('genre/', views.Genres.as_view()),
    path('movieDetail/<int:pk>', views.MovieDetail.as_view()),
    path('addReview/', views.add_review),
    path('movieReviews/', views.get_movie_reviews),
    path('topRatedMovies/', views.TopRatedMovies.as_view()),
    path('mostUpvotedMovies/', views.MostUpvotedMovies.as_view()),
    path('filteredMovies/', views.get_filtered_movies),
    path('searchMovies/', views.search_movie),
    path('searchCast/', views.search_cast),
    path('addActor/', views.add_actor),
    path('addDirector/', views.add_director),
    path('upvoteMovie/', views.upvote_movie),
    path('downvoteMovie/', views.downvote_movie),
    path('movieDetails/', views.get_movie_details),
    path('bookmarkMovie/', views.bookmark_movie),
    path('removeBookmark/', views.remove_bookmark),
]
