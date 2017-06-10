# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caramella', '0008_remito_preciototal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remito',
            name='archivo',
            field=models.CharField(max_length=200, verbose_name=b'Archivo'),
        ),
    ]
