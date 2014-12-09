# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paper', '0002_auto_20141208_2307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sourcehistory',
            old_name='souce',
            new_name='source',
        ),
        migrations.AlterField(
            model_name='source',
            name='current_version',
            field=models.ForeignKey(related_name='canonical_source', blank=True, to='paper.SourceHistory', null=True),
            preserve_default=True,
        ),
    ]
