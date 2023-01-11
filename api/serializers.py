from rest_framework import serializers
from .models import Cast, Comment, Movie, Review, User, Recommend, Tags
import json
from django.forms.models import model_to_dict


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'name',
            'profile_pic_url'
        ]


class UserInforSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'name',
            'profile_pic_url'
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = [
            'id',
            'genre',
        ]


class MovieDetailSerializer(serializers.ModelSerializer):

    director_name = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    actor_name = serializers.SerializerMethodField()

    def get_actor_name(self, instance):
        result = []
        for actor in instance.actors.all():
            m = {
                "name": actor.name,
                "image": actor.profile_pic_url
            }
            result.append(m)
        return result

    def get_genres(self, instance):
        return [tag.genre for tag in instance.tag.all()]

    def get_director_name(self, instance):
        result = []
        for actor in instance.director.all():
            m = {
                "id": actor.id,
                "name": actor.name,
                "image": actor.profile_pic_url
            }
            result.append(m)
        return result

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'year',
            'storyline',
            'duration',
            'rating',
            'number_of_reviews',
            'imageUrl',
            'cardImageUrl',
            'director',
            'actors',
            'trailer_url',
            'tag',
            'director_name',
            'actor_name',
            'genres',
        ]


class MovieOverviewSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    def get_genres(self, instance):
        return [tag.genre for tag in instance.tag.all()]

    class Meta:
        model = Movie
        fields = [
            'id',
            'imageUrl',
            'genres'
        ]


class NewMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'year',
            'duration',
            'storyline',
            'imageUrl',
            'cardImageUrl',
            'trailer_url',
            'tag',
        ]


class MovieFilterSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    def get_genres(self, instance):
        return [tag.genre for tag in instance.tag.all()]

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'year',
            'rating',
            'duration',
            'imageUrl',
            'genres'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    profile_pic_url = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    upvoted = serializers.SerializerMethodField()

    def get_upvoted(self,instance):
        user_id = self.context.get("user_id")
        user_instance = User.objects.get(pk=user_id)
        if instance.upvoted_by.contains(user_instance):
            return True;
        return False;

    def get_name(self, instance):
        return instance.user.name

    def get_profile_pic_url(self, instance):
        return instance.user.profile_pic_url

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'name',
            'profile_pic_url',
            'movie',
            'description',
            'rating',
            'date',
            'upvote',
            'upvoted_by',
            'upvoted',
        ]


class CastSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, instance):
        return instance.profile_pic_url

    class Meta:
        model = Cast
        fields = [
            'id',
            'name',
            'image',
        ]

class NewCastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = [
            'id',
            'name',
            'profile_pic_url',
        ]


class UserMovieDetailSerializer(serializers.ModelSerializer):

    director_name = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    actor_name = serializers.SerializerMethodField()
    upvoted = serializers.SerializerMethodField()
    bookmarked = serializers.SerializerMethodField()

    def get_bookmarked(self, instance):
        user_id = self.context.get("user_id")
        user_instance = User.objects.get(pk=user_id)
        if (instance.bookmarked_by.contains(user_instance)):
            return True
        return False

    def get_upvoted(self, instance):
        user_id = self.context.get("user_id")
        user_instance = User.objects.get(pk=user_id)
        if (instance.upvoted_by.contains(user_instance)):
            return True
        return False

    def get_actor_name(self, instance):
        result = []
        for actor in instance.actors.all():
            m = {
                "name": actor.name,
                "image": actor.profile_pic_url
            }
            result.append(m)
        return result

    def get_genres(self, instance):
        return [tag.genre for tag in instance.tag.all()]

    def get_director_name(self, instance):
        result = []
        for actor in instance.director.all():
            m = {
                "id": actor.id,
                "name": actor.name,
                "image": actor.profile_pic_url
            }
            result.append(m)
        return result

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'year',
            'storyline',
            'duration',
            'rating',
            'number_of_reviews',
            'imageUrl',
            'cardImageUrl',
            'director',
            'actors',
            'trailer_url',
            'tag',
            'director_name',
            'actor_name',
            'genres',
            'upvoted',
            'bookmarked',
        ]
