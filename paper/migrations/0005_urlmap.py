# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import paucore.data.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0004_auto_20141209_0804'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('raw_url', models.CharField(max_length=255, unique=True, null=True, blank=True)),
                ('canonical_url', models.CharField(max_length=255, unique=True, null=True, blank=True)),
                ('created', paucore.data.fields.CreateDateTimeField(default=datetime.datetime.utcnow, blank=True)),
                ('updated', paucore.data.fields.LastModifiedDateTimeField(blank=True)),
                ('extra', paucore.data.fields.DictField(default=dict, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
