# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slider', '0002_shitstormindexpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shitstorm',
            name='body',
        ),
    ]
