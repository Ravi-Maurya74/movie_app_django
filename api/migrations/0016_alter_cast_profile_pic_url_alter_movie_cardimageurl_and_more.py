# Generated by Django 4.1.2 on 2022-12-24 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_movie_cardimageurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cast',
            name='profile_pic_url',
            field=models.URLField(max_length=250),
        ),
        migrations.AlterField(
            model_name='movie',
            name='cardImageUrl',
            field=models.URLField(max_length=250),
        ),
        migrations.AlterField(
            model_name='movie',
            name='imageUrl',
            field=models.URLField(max_length=250),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_pic_url',
            field=models.URLField(blank=True, max_length=250),
        ),
    ]
