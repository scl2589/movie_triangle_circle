# Generated by Django 2.1.15 on 2020-06-14 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20200614_1942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='rank_users',
        ),
        migrations.AddField(
            model_name='movie',
            name='rank',
            field=models.FloatField(null=True),
        ),
    ]
