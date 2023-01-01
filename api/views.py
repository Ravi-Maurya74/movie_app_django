from rest_framework import generics
from .models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.db.models import Q
from .models import Cast, Comment, Movie, Review, User, Recommend, Tags
from .serializers import CreateUserSerializer, GenreSerializer, MovieDetailSerializer, ReviewSerializer, UserInforSerializer, MovieOverviewSerializer, CastSerializer, MovieFilterSerializer

# Create your views here.


class NewUser(generics.CreateAPIView):
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
    data = ReviewSerializer(rev).data
    return Response(data)


@api_view(['POST'])
def get_movie_reviews(request):
    received_json_data = json.loads(request.body)
    movie_instance = Movie.objects.get(pk=received_json_data['movie_id'])
    reviews_instance = Review.objects.filter(movie=movie_instance)
    data = ReviewSerializer(reviews_instance, many=True).data
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
    cast_instance = Cast.objects.filter(name__icontains=received_json_data['name'])[:5]
    data = CastSerializer(cast_instance,many=True).data
    return Response(data)