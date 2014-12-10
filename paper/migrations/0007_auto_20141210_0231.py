# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0006_remove_article_raw_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='origin',
            field=models.ForeignKey(blank=True, to='paper.Origin', null=True),
            preserve_default=True,
        ),
    ]
