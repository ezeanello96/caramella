# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('caramella', '0003_auto_20170523_1505'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lata',
            options={'ordering': ('codigo', 'lote', 'gusto'), 'verbose_name': 'Lata', 'verbose_name_plural': 'Latas'},
        ),
        migrations.AlterField(
            model_name='lata',
            name='fecha_elab',
            field=models.DateField(auto_now_add=True, verbose_name=b'Fecha de elaboraci\xc3\xb3n'),
        ),
    ]
