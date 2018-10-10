# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 16:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0006_auto_20171120_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sublist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(db_index=True, default=999)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qa.TestList')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='qa.TestList')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='sublist',
            unique_together=set([('parent', 'child')]),
        ),
    ]
