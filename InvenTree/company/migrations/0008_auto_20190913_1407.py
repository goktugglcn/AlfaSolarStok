# Generated by Django 2.2.5 on 2019-09-13 14:07

import InvenTree.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_remove_supplierpart_lead_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='URL',
            field=InvenTree.fields.InvenTreeURLField(blank=True, help_text='Link to external company information'),
        ),
        migrations.AlterField(
            model_name='supplierpart',
            name='URL',
            field=InvenTree.fields.InvenTreeURLField(blank=True, help_text='URL for external supplier part link'),
        ),
    ]
