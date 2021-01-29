# Generated by Django 2.1.15 on 2021-01-27 02:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('units', '0017_auto_20210126_2104'),
        ('service_log', '0026_auto_20210126_2104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fault',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occurred', models.DateTimeField(db_index=True, default=django.utils.timezone.now, help_text='When did this fault occur. Format DD MMM YYYY hh:mm (hh:mm is 24h time e.g. 31 May 2012 14:30)', verbose_name='Date & Time fault occurred')),
                ('reviewed', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='fault_events_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-occurred',),
                'permissions': (('can_review', 'Can review faults'),),
            },
        ),
        migrations.CreateModel(
            name='FaultType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Enter the fault code or number', max_length=255, unique=True, verbose_name='code')),
                ('slug', models.SlugField(editable=False, help_text='Unique URL friendly identifier made of lowercase characters, dashes, and underscores.', max_length=255, unique=True)),
                ('description', models.TextField(blank=True, help_text='Enter a description for this fault type', verbose_name='description')),
            ],
            options={
                'ordering': ('code',),
            },
        ),
        migrations.AddField(
            model_name='fault',
            name='fault_type',
            field=models.ForeignKey(help_text='Select the fault type that occurred', on_delete=django.db.models.deletion.PROTECT, to='faults.FaultType', verbose_name='fault type'),
        ),
        migrations.AddField(
            model_name='fault',
            name='modality',
            field=models.ForeignKey(blank=True, help_text='Select the modality being used when this fault occurred (optional)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='faults', to='units.Modality', verbose_name='modality'),
        ),
        migrations.AddField(
            model_name='fault',
            name='modified_by',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='fault_events_modified', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fault',
            name='related_service_events',
            field=models.ManyToManyField(blank=True, help_text='Enter the service event IDs of any related service events.', to='service_log.ServiceEvent', verbose_name='related service events'),
        ),
        migrations.AddField(
            model_name='fault',
            name='reviewed_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fault_reviewer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fault',
            name='treatment_technique',
            field=models.ForeignKey(blank=True, help_text='Select the treatment technique being used when this fault occurred (optional)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='faults', to='units.TreatmentTechnique', verbose_name='treatment technique'),
        ),
        migrations.AddField(
            model_name='fault',
            name='unit',
            field=models.ForeignKey(help_text='Select the unit this fault occurred on', on_delete=django.db.models.deletion.CASCADE, related_name='faults', to='units.Unit', verbose_name='unit'),
        ),
    ]