# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stencil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('NAME', models.CharField(max_length=100)),
                ('WQAR_737_7', models.CharField(max_length=1000)),
                ('WQAR_737_3C', models.CharField(max_length=1000)),
                ('ATA', models.IntegerField()),
                ('CREATOR', models.CharField(max_length=100)),
                ('echarts_737_7', models.CharField(max_length=1000)),
                ('echarts_737_3C', models.CharField(max_length=1000)),
            ],
        ),
    ]
