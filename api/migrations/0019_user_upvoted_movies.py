# Generated by Django 4.1.2 on 2023-01-02 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_movie_storyline_alter_movie_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='upvoted_movies',
            field=models.ManyToManyField(related_name='upvoted_by', to='api.movie'),
        ),
    ]
