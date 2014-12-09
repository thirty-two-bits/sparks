# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0003_auto_20141209_0143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source',
            name='content_hash',
        ),
        migrations.RemoveField(
            model_name='sourcehistory',
            name='content_hash',
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.TextField(max_length=1000, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='kind',
            field=models.IntegerField(default=1, null=True, blank=True, choices=[(1, b'rss'), (2, b'buzz sumo')]),
            preserve_default=True,
        ),
    ]
