# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-26 08:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20160926_0828'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='author',
            table='Author',
        ),
    ]
