# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('razon_social', models.CharField(max_length=50, verbose_name=b'Razon Social')),
                ('precio', models.FloatField(verbose_name=b'Precio por Kilogramo')),
                ('direccion', models.CharField(max_length=40, verbose_name=b'Direcci\xc3\xb3n')),
                ('telefono', models.CharField(max_length=20, verbose_name=b'Telefono')),
                ('cuit', models.CharField(max_length=20, verbose_name=b'CUIT')),
                ('localidad', models.CharField(max_length=20, verbose_name=b'Localidad')),
            ],
            options={
                'ordering': ('cuit', 'razon_social'),
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20, verbose_name=b'Nombre')),
            ],
            options={
                'ordering': ('nombre',),
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
            },
        ),
        migrations.CreateModel(
            name='Gusto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20, verbose_name=b'Nombre')),
                ('grupo', models.ForeignKey(to='caramella.Grupo')),
            ],
            options={
                'ordering': ('grupo', 'nombre'),
                'verbose_name': 'Gusto',
                'verbose_name_plural': 'Gustos',
            },
        ),
        migrations.CreateModel(
            name='Lata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('peso', models.FloatField(verbose_name=b'Peso')),
                ('codigo', models.CharField(unique=True, max_length=255, verbose_name=b'Codigo de barras')),
                ('lote', models.CharField(max_length=20, verbose_name=b'Lote')),
                ('numero', models.IntegerField(verbose_name=b'Numero de producto')),
                ('fecha_elab', models.DateField(verbose_name=b'Fecha de elaboraci\xc3\xb3n')),
                ('en_stock', models.BooleanField(verbose_name=True)),
                ('gusto', models.ForeignKey(to='caramella.Gusto')),
            ],
            options={
                'ordering': ('en_stock', 'lote', 'gusto'),
                'verbose_name': 'Lata',
                'verbose_name_plural': 'Latas',
            },
        ),
        migrations.CreateModel(
            name='Remito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(verbose_name=b'Fecha')),
                ('archivo', models.FileField(upload_to=b'remitos/', verbose_name=b'Archivo')),
                ('cliente', models.ForeignKey(to='caramella.Cliente')),
                ('latas', models.ManyToManyField(to='caramella.Lata')),
            ],
            options={
                'ordering': ('fecha', 'cliente'),
                'verbose_name': 'Remito',
                'verbose_name_plural': 'Remitos',
            },
        ),
    ]
