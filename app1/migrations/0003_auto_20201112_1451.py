# Generated by Django 2.2.4 on 2020-11-12 11:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_grantedwish_the_time_wish_was_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='grantedwish',
            name='desc',
            field=models.CharField(default=' ', max_length=255),
        ),
        migrations.AddField(
            model_name='pendingwish',
            name='desc',
            field=models.CharField(default=' ', max_length=255),
        ),
        migrations.AlterField(
            model_name='grantedwish',
            name='the_time_wish_was_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 12, 14, 51, 54, 631523)),
        ),
    ]
