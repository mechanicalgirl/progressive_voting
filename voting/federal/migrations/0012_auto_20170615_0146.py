# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-15 01:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('federal', '0011_district_type'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='district',
            unique_together=set([('state', 'district', 'type')]),
        ),
    ]