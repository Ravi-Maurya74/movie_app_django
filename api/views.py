from rest_framework import generics, status
from .models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.db.models import Q
from .models import Cast, Comment, Movie, Review, User, Recommend, Tags
from .serializers import CreateUserSerializer, GenreSerializer, MovieDetailSerializer, ReviewSerializer, UserInforSerializer, MovieOverviewSerializer, CastSerializer, MovieFilterSerializer, UserMovieDetailSerializer, NewCastSerializer, NewMovieSerializer

# Create your views here.


class NewUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserInforSerializer


class IdentifyUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserInforSerializer


@api_view(['POST'])
def login(request):
    received_json_data = json.loads(request.body)
    user_instance = None
    try:
        user_instance = User.objects.get(email=received_json_data['email'])
    except:
        return Response({'status': 400, 'prompt': 'Email not registered.'})

    if user_instance.password != received_json_data['password']:
        return Response({'status': 400, 'prompt': 'Invalid password.'})

    data = UserInforSerializer(user_instance).data
    return Response({'status': 200, 'data': data})


class Genres(generics.ListAPIView):
    queryset = Tags.objects.all()
    serializer_class = GenreSerializer


class MovieDetail(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer


class NewMovie(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = NewMovieSerializer


class TopRatedMovies(generics.ListAPIView):
    queryset = Movie.objects.all().order_by('-rating')
    serializer_class = MovieOverviewSerializer


class MostUpvotedMovies(generics.ListAPIView):
    queryset = Movie.objects.all().order_by('-upvotes')
    serializer_class = MovieOverviewSerializer


@api_view(['POST'])
def add_review(request):
    received_json_data = json.loads(request.body)
    user_instance = User.objects.get(pk=received_json_data['user_id'])
    movie_instance = Movie.objects.get(pk=received_json_data['movie_id'])
    rating = received_json_data['rating']
    description = received_json_data['description']
    total = movie_instance.number_of_reviews*movie_instance.rating
    total += rating
    movie_instance.number_of_reviews += 1
    movie_instance.rating = total/movie_instance.number_of_reviews
    movie_instance.save()
    rev = Review(user=user_instance, movie=movie_instance,
                 rating=rating, description=description)
    rev.save()
    data = ReviewSerializer(rev, context={
        "user_id": received_json_data['user_id']}).data
    return Response(data)


@api_view(['POST'])
def get_movie_reviews(request):
    received_json_data = json.loads(request.body)
    movie_instance = Movie.objects.get(pk=received_json_data['movie_id'])
    reviews_instance = Review.objects.filter(
        movie=movie_instance).order_by('-upvote')
    data = ReviewSerializer(reviews_instance, many=True, context={
        "user_id": received_json_data['user_id']}).data
    return Response(data)


@api_view(['POST'])
def get_filtered_movies(request):
    received_json_data = json.loads(request.body)
    filter_genres = received_json_data['filters']
    movies_intance = Movie.objects.all()
    for filter in filter_genres:
        tag_instance = Tags.objects.get(pk=filter)
        movies_intance = movies_intance.filter(tag=tag_instance)
    data = MovieFilterSerializer(movies_intance, many=True).data
    return Response(data)


@api_view(['POST'])
def search_movie(request):
    received_json_data = json.loads(request.body)
    movies_instance = Movie.objects.filter(
        title__icontains=received_json_data['title'])[:5]
    data = MovieFilterSerializer(movies_instance, many=True).data
    return Response(data)


@api_view(['POST'])
def search_cast(request):
    received_json_data = json.loads(request.body)
    cast_instance = Cast.objects.filter(
        name__icontains=received_json_data['name'])[:5]
    data = CastSerializer(cast_instance, many=True).data
    return Response(data)


@api_view(['POST'])
def add_actor(request):
    received_json_data = json.loads(request.body)
    movie_instance = Movie.objects.get(pk=received_json_data['movie_id'])
    actor_instance = Cast.objects.get(pk=received_json_data['cast_id'])
    movie_instance.actors.add(actor_instance)
    movie_instance.save()
    data = MovieDetailSerializer(movie_instance).data
    return Response(data)


@api_view(['POST'])
def add_director(request):
    received_json_data = json.loads(request.body)
    movie_instance = Movie.objects.get(pk=received_json_data['movie_id'])
    actor_instance = Cast.objects.get(pk=received_json_data['cast_id'])
    movie_instance.director.add(actor_instance)
    movie_instance.save()
    data = MovieDetailSerializer(movie_instance).data
    return Response(data)


@api_view(['POST'])
def upvote_movie(request):
    received_json_data = json.loads(request.body)
    movie_instance = Movie.objects.get(pk=received_json_data['movie_id'])
    user_instance = User.objects.get(pk=received_json_data['user_id'])
    if user_instance.upvoted_movies.contains(movie_instance):
        return Response({"error": "Already upvoted."}, status=status.HTTP_400_BAD_REQUEST)
    user_instance.upvoted_movies.add(movie_instance)
    movie_instance.upvotes += 1
    user_instance.save()
    movie_instance.save()
    return Response({"message": "Upvoted successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def downvote_movie(request):
    received_json_data = json.loads(request.body)
    movie_instance = Movie.objects.get(pk=received_json_data['movie_id'])
    user_instance = User.objects.get(pk=received_json_data['user_id'])
    if user_instance.upvoted_movies.contains(movie_instance):
        user_instance.upvoted_movies.remove(movie_instance)
        movie_instance.upvotes -= 1
        user_instance.save()
        movie_instance.save()
        return Response({"message": "Downvoted successfully"}, status=status.HTTP_200_OK)
    return Response({"error": "Already downvoted."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_movie_details(request):
    received_json_data = json.loads(request.body)
    movie_instance = Movie.objects.get(pk=received_json_data['movie_id'])
    data = UserMovieDetailSerializer(movie_instance, context={
                                     "user_id": received_json_data['user_id']}).data
    return Response(data)


@api_view(['POST'])
def bookmark_movie(request):
    received_json_data = json.loads(request.body)
    movie_instance = Movie.objects.get(pk=received_json_data['movie_id'])
    user_instance = User.objects.get(pk=received_json_data['user_id'])
    if user_instance.bookmarked_movies.contains(movie_instance):
        return Response({"error": "Already in bookmarks"}, status=status.HTTP_400_BAD_REQUEST)
    user_instance.bookmarked_movies.add(movie_instance)
    user_instance.save()
    movie_instance.save()
    return Response({"message": "Successful added to bookmarks."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def remove_bookmark(request):
    received_json_data = json.loads(request.body)
    movie_instance = Movie.objects.get(pk=received_json_data['movie_id'])
    user_instance = User.objects.get(pk=received_json_data['user_id'])
    if user_instance.bookmarked_movies.contains(movie_instance):
        user_instance.bookmarked_movies.remove(movie_instance)
        user_instance.save()
        movie_instance.save()
        return Response({"message": "Removed from bookmarks."}, status=status.HTTP_200_OK)
    return Response({"error": "Movie is not in bookmarks."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def upvote_review(request):
    received_json_data = json.loads(request.body)
    review_instance = Review.objects.get(pk=received_json_data['review_id'])
    user_instance = User.objects.get(pk=received_json_data['user_id'])
    if review_instance.upvoted_by.contains(user_instance):
        return Response({"error": "Already upvoted."}, status=status.HTTP_400_BAD_REQUEST)
    review_instance.upvoted_by.add(user_instance)
    review_instance.upvote += 1
    user_instance.save()
    review_instance.save()
    return Response({"message": "Upvoted successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def downvote_review(request):
    received_json_data = json.loads(request.body)
    review_instance = Review.objects.get(pk=received_json_data['review_id'])
    user_instance = User.objects.get(pk=received_json_data['user_id'])
    if review_instance.upvoted_by.contains(user_instance):
        review_instance.upvoted_by.remove(user_instance)
        review_instance.upvote -= 1
        user_instance.save()
        review_instance.save()
        return Response({"message": "Downvoted successfully"}, status=status.HTTP_200_OK)
    return Response({"error": "Already downvoted."}, status=status.HTTP_400_BAD_REQUEST)


class CreateNewCast(generics.CreateAPIView):
    queryset = Cast.objects.all()
    serializer_class = NewCastSerializer


@api_view(['POST'])
def bookmarked_movies(request):
    received_json_data = json.loads(request.body)
    user_instance = User.objects.get(pk=received_json_data['user_id'])
    movies_instance = user_instance.bookmarked_movies.all()
    data = MovieFilterSerializer(movies_instance, many=True).data
    return Response(data)


@api_view(['POST'])
def edit_account_info(request):
    received_json_data = json.loads(request.body)
    user_instance = User.objects.get(pk=received_json_data['user_id'])
    change_name = received_json_data['change_name']
    change_profile_pic = received_json_data['change_profile_pic']
    if change_name:
        user_instance.name = received_json_data['name']
    if change_profile_pic:
        user_instance.profile_pic_url = received_json_data['profile_pic_url']
    user_instance.save()
    return Response({'status': 'Account info updated'})
