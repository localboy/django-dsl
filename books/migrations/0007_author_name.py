# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-26 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_auto_20160926_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='name',
            field=models.CharField(default=None, max_length=200),
        ),
    ]