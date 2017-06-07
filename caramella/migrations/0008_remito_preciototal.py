# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caramella', '0007_remito_pesototal'),
    ]

    operations = [
        migrations.AddField(
            model_name='remito',
            name='precioTotal',
            field=models.FloatField(default=0, verbose_name=b'Precio total ($)'),
            preserve_default=False,
        ),
    ]
