# Generated by Django 2.1.15 on 2020-06-14 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_review_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rank',
            field=models.FloatField(null=True),
        ),
    ]
