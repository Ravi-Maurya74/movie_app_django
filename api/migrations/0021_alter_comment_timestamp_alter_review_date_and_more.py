# Generated by Django 4.1.2 on 2023-01-06 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_user_bookmarked_movies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='upvoted_by',
            field=models.ManyToManyField(blank=True, related_name='upvoted_reviews', to='api.user'),
        ),
    ]
