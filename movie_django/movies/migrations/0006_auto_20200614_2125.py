# Generated by Django 2.1.15 on 2020-06-14 12:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0005_auto_20200614_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='rank',
        ),
        migrations.AddField(
            model_name='movie',
            name='rank_users',
            field=models.ManyToManyField(related_name='user_rank', through='movies.UserRank', to=settings.AUTH_USER_MODEL),
        ),
    ]
