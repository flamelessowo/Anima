# Generated by Django 3.2.5 on 2021-08-22 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coresite', '0015_auto_20210822_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='anime',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='coresite.anime'),
        ),
    ]
