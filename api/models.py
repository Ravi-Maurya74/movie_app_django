from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import timedelta

# Create your models here.


class Cast(models.Model):
    name = models.CharField(max_length=50)
    profile_pic_url = models.URLField(max_length=250)

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    duration = models.DurationField(default=timedelta(hours=0, minutes=0))
    storyline = models.CharField(max_length=500)
    imageUrl = models.URLField(max_length=250)
    cardImageUrl = models.URLField(max_length=250)
    director = models.ManyToManyField(
        Cast, related_name='directed', blank=True)
    actors = models.ManyToManyField(Cast, related_name='acted', blank=True)
    trailer_url = models.URLField(blank=True, null=True)
    tag = models.ManyToManyField(
        'Tags', related_name='movie', blank=True)
    rating = models.FloatField(default=0)
    number_of_reviews = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    

    def __str__(self) -> str:
        return self.title


class User(models.Model):
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    profile_pic_url = models.URLField(blank=True, max_length=250)

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    user = models.ForeignKey(
        User, related_name='review', on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie, related_name='review', on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    description = models.CharField(max_length=400)
    date = models.DateField(auto_now=True)
    upvote = models.IntegerField(default=0)
    upvoted_by = models.ManyToManyField(User,related_name='upvoted_reviews')

    def __str__(self) -> str:
        return self.description[0:30]


class Recommend(models.Model):
    user = models.ForeignKey(
        User, related_name='recommend', on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie, related_name='recommend', on_delete=models.CASCADE)
    value = models.IntegerField(
        validators=[MinValueValidator(-1), MaxValueValidator(1)]
    )

    def __str__(self) -> str:
        return f'{self.user} {self.movie}'


class Comment(models.Model):
    user = models.ForeignKey(
        User, related_name='comment', on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie, related_name='comment', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=200)
    liked_by = models.ManyToManyField(
        User, related_name='comments', blank=True)
    replied_to = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='reply')
    upvote = models.IntegerField(default=0)
    upvoted_by = models.ManyToManyField(User,related_name='upvoted_comments')

    def __str__(self) -> str:
        return self.comment[0:30]


class Tags(models.Model):
    genre = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.genre
