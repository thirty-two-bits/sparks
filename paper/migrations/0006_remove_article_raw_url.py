# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0005_urlmap'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='raw_url',
        ),
    ]
