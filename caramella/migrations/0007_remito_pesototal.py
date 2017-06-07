# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caramella', '0006_auto_20170530_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='remito',
            name='pesoTotal',
            field=models.FloatField(default=0, verbose_name=b'Peso total'),
            preserve_default=False,
        ),
    ]
