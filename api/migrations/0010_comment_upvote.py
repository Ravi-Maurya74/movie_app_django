# Generated by Django 4.1.2 on 2022-12-21 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_movie_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='upvote',
            field=models.IntegerField(default=0),
        ),
    ]
