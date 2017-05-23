# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('caramella', '0004_auto_20170523_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='activo',
            field=models.BooleanField(default=True, verbose_name=b'Cliente activo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gusto',
            name='activo',
            field=models.BooleanField(default=True, verbose_name=b'Gusto activo'),
            preserve_default=False,
        ),
    ]
