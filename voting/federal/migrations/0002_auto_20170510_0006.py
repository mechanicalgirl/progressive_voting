# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-10 00:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('federal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='tweet_text',
            field=models.TextField(blank=True, max_length=135, null=True),
        ),
    ]