# Generated by Django 3.2.5 on 2021-08-16 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coresite', '0011_playervideo'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='slug',
            field=models.SlugField(default='dummy-slug', verbose_name='Slug'),
        ),
    ]