# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import paucore.data.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SourceHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', paucore.data.fields.CreateDateTimeField(default=datetime.datetime.utcnow, blank=True)),
                ('updated', paucore.data.fields.LastModifiedDateTimeField(blank=True)),
                ('extra', paucore.data.fields.DictField(default=dict, editable=False)),
                ('etag', models.CharField(max_length=255, null=True, blank=True)),
                ('content_hash', models.CharField(max_length=255, null=True, blank=True)),
                ('content', models.TextField(null=True, blank=True)),
                ('souce', models.ForeignKey(blank=True, to='paper.Source', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='source',
            name='content_hash',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='source',
            name='current_version',
            field=models.ForeignKey(blank=True, to='paper.SourceHistory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='source',
            name='etag',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='source',
            name='needs_update',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='source',
            name='url',
            field=models.CharField(max_length=255, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
