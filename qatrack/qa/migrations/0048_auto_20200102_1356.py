# Generated by Django 2.1.11 on 2020-01-02 18:56

from django.db import migrations, models

import qatrack.qatrack_core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0047_fix_serialized_uploads'),
    ]

    operations = [
        migrations.AddField(
            model_name='testinstance',
            name='json_value',
            field=qatrack.qatrack_core.fields.JSONField(blank=True, editable=True, help_text='Currently used to store results of upload file analysis. Allows you to retrieve results of file upload analysis without having to reanalyze the file', null=True),
        ),
    ]