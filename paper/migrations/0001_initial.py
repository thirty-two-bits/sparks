# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import paucore.data.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('url', models.CharField(max_length=255, unique=True, null=True, blank=True)),
                ('raw_url', models.CharField(max_length=255, unique=True, null=True, blank=True)),
                ('processed', models.BooleanField(default=False)),
                ('created', paucore.data.fields.CreateDateTimeField(default=datetime.datetime.utcnow, blank=True)),
                ('updated', paucore.data.fields.LastModifiedDateTimeField(blank=True)),
                ('origin', models.IntegerField(null=True, blank=True)),
                ('extra', paucore.data.fields.DictField(default=dict, editable=False)),
                ('init_twitter_shares', models.IntegerField(null=True, blank=True)),
                ('init_facebook_shares', models.IntegerField(null=True, blank=True)),
                ('init_pinterest_shares', models.IntegerField(null=True, blank=True)),
                ('init_total_shares', models.IntegerField(null=True, blank=True)),
                ('current_twitter_shares', models.IntegerField(null=True, blank=True)),
                ('current_facebook_shares', models.IntegerField(null=True, blank=True)),
                ('current_pinterest_shares', models.IntegerField(null=True, blank=True)),
                ('current_total_shares', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Origin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('url', models.CharField(max_length=255, unique=True, null=True, blank=True)),
                ('created', paucore.data.fields.CreateDateTimeField(default=datetime.datetime.utcnow, blank=True)),
                ('updated', paucore.data.fields.LastModifiedDateTimeField(blank=True)),
                ('source', models.IntegerField(null=True, blank=True)),
                ('kind', models.IntegerField(default=1, null=True, blank=True, choices=[(1, b'curated'), (2, b'rss feed')])),
                ('extra', paucore.data.fields.DictField(default=dict, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('kind', models.IntegerField(default=1, null=True, blank=True, choices=[(1, b'curated'), (2, b'rss feed')])),
                ('update_freq', models.IntegerField(default=5, null=True, blank=True)),
                ('failure_count', models.IntegerField(default=0, null=True, blank=True)),
                ('status', models.IntegerField(default=10, null=True, blank=True, choices=[(10, b'Active'), (20, b'Disabled'), (30, b'Disabled for failures')])),
                ('last_update', models.DateTimeField(auto_now_add=True, null=True)),
                ('next_update', models.DateTimeField(auto_now_add=True, null=True)),
                ('created', paucore.data.fields.CreateDateTimeField(default=datetime.datetime.utcnow, blank=True)),
                ('updated', paucore.data.fields.LastModifiedDateTimeField(blank=True)),
                ('extra', paucore.data.fields.DictField(default=dict, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
