# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-19 21:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device_log', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
