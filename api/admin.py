from django.contrib import admin
from .models import Cast, Comment, Movie, User, Review, Recommend, Tags

# Register your models here.


class Reviewview(admin.ModelAdmin):
    readonly_fields = ('date',)


class CastView(admin.ModelAdmin):
    readonly_fields = ('id',)


class TagView(admin.ModelAdmin):
    readonly_fields = ('movies', 'id')

    def movies(self, instance):
        return [f'{m.title}' for m in instance.movie.all()]


class UserView(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Cast, CastView)
admin.site.register(Comment)
admin.site.register(Movie)
admin.site.register(User, UserView)
admin.site.register(Review, Reviewview)
admin.site.register(Recommend)
admin.site.register(Tags, TagView)
