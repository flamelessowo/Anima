# Generated by Django 3.2.5 on 2021-08-26 08:00

import coresite.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coresite', '0021_auto_20210826_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(upload_to=coresite.models.Video.content_file_name),
        ),
        migrations.CreateModel(
            name='UserAnimeRationg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, 'Insignificantly'), (2, 'Ugly'), (3, 'Bad'), (4, 'Anyhow'), (5, 'Mediocre'), (6, 'Not bad'), (7, 'Good'), (8, 'Great'), (9, 'Superb'), (10, 'Masterpiece')])),
                ('anime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coresite.anime')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]