# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-18 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20170718_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='users/default_profile.png', upload_to='users/%Y/%M/%d/'),
        ),
    ]