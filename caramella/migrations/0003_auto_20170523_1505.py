# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('caramella', '0002_remove_lata_numero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lata',
            name='en_stock',
            field=models.BooleanField(verbose_name=b'En stock'),
        ),
    ]
