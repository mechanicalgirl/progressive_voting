# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-09 22:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('incumbent', models.BooleanField(default=False)),
                ('running', models.BooleanField(default=False)),
                ('party', models.CharField(choices=[('D', 'Democrat'), ('R', 'Republican'), ('G', 'Green'), ('O', 'Other')], max_length=1)),
                ('position', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('twitter_handle', models.CharField(blank=True, max_length=100, null=True)),
                ('tweet_text', models.CharField(blank=True, max_length=135, null=True)),
                ('facebook_url', models.CharField(blank=True, max_length=200, null=True)),
                ('facebook_text', models.TextField(blank=True, null=True)),
                ('reasons_to_keep', models.TextField(blank=True, null=True)),
                ('reasons_to_vote_out', models.TextField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2)),
                ('district', models.CharField(default='Senate', max_length=8)),
                ('next_primary_date', models.DateField(blank=True, null=True, verbose_name='Next Primary')),
                ('next_early_vote_date_begin', models.DateField(blank=True, null=True, verbose_name='Early Voting Begins')),
                ('next_early_vote_date_end', models.DateField(blank=True, null=True, verbose_name='Early Voting Ends')),
                ('next_election_date', models.DateField(blank=True, null=True, verbose_name='Election Date')),
            ],
            options={
                'ordering': ['state', 'district'],
            },
        ),
        migrations.CreateModel(
            name='VoterRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2, unique=True)),
                ('url', models.CharField(max_length=200)),
                ('last_updated_date', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.AddField(
            model_name='district',
            name='voter_reg_url',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='federal.VoterRegistration'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='federal.District'),
        ),
        migrations.AlterUniqueTogether(
            name='district',
            unique_together=set([('state', 'district')]),
        ),
    ]
