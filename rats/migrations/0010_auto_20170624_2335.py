# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-24 15:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rats', '0009_auto_20170624_2316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='residency',
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
    ]