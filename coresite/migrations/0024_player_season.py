# Generated by Django 3.2.5 on 2021-08-27 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coresite', '0023_rename_useranimerationg_useranimerating'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='season',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]