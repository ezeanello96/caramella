# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('caramella', '0005_auto_20170523_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='gusto',
            name='rna',
            field=models.CharField(default=None, max_length=50, verbose_name=b'Nro RNA'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gusto',
            name='rne',
            field=models.CharField(default=None, max_length=50, verbose_name=b'Nro RNE'),
            preserve_default=False,
        ),
    ]
