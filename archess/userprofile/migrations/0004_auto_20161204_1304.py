# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-04 11:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_auto_20161204_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistics',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
