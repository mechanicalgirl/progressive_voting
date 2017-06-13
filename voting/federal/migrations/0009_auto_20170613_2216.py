# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-13 22:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('federal', '0008_messages'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messages',
            options={'ordering': ['active', 'posted', '-date_to_post'], 'verbose_name_plural': 'messages'},
        ),
        migrations.AddField(
            model_name='candidate',
            name='candidate_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
