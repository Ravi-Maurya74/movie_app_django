# Generated by Django 4.1.2 on 2022-12-24 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_user_profile_pic_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='cardImageUrl',
            field=models.URLField(default='https://static1.colliderimages.com/wordpress/wp-content/uploads/2022/09/the-dark-knight-feature.jpeg'),
            preserve_default=False,
        ),
    ]
