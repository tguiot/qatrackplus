# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-05 19:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0005_auto_20170505_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='issuetag',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
