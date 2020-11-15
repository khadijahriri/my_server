# Generated by Django 2.2.4 on 2020-11-14 09:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_auto_20201112_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='grantedwish',
            name='users_who_like_this_wish',
            field=models.ManyToManyField(related_name='liked_wishes', to='app1.User'),
        ),
        migrations.AlterField(
            model_name='grantedwish',
            name='the_time_wish_was_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 14, 12, 33, 8, 181487)),
        ),
    ]