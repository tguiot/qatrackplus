# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-25 19:51
from __future__ import unicode_literals
import logging

from django.db import migrations

logger = logging.getLogger("qatrack.migrations")


def check_uploads(apps, schema_editor):
    from qatrack.qa.models import UPLOAD

    Test = apps.get_model("qa", "Test")
    uploads = Test.objects.filter(type=UPLOAD, calculation_procedure__contains="FILE")

    if uploads.exists():
        msg = (
            "Note: if any of the following tests process binary files (e.g. images, "
            "dicom files etc) rather than plain text, you must edit the calculation "
            "and replace 'FILE' with 'BIN_FILE'. Tests:\n%s"
        ) % ("\n".join("\t%s (%s)," % (u.name, u.slug) for u in uploads))
        logger.info(msg)
        print(msg)


def check_back(apps, schema_editor):
    from qatrack.qa.models import UPLOAD

    Test = apps.get_model("qa", "Test")
    uploads = Test.objects.filter(type=UPLOAD, calculation_procedure__contains="BIN_FILE")

    if uploads.exists():
        msg = (
            "Note: if any of the following tests process binary files (e.g. images, "
            "dicom files etc) rather than plain text, you must edit the calculation "
            "and replace 'BIN_FILE' with 'FILE'. Tests:\n%s"
        ) % ("\n".join("\t%s (%s)," % (u.name, u.slug) for u in uploads))
        logger.info(msg)
        print(msg)


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0013_auto_20180511_2341'),
    ]

    operations = [
        migrations.RunPython(check_uploads, check_back),
    ]
