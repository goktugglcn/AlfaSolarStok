# Generated by Django 3.2.19 on 2023-05-13 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0094_auto_20230514_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesordershipment',
            name='delivery_date',
            field=models.DateField(blank=True, help_text='Date of delivery of shipment', null=True, verbose_name='Delivery Date'),
        ),
    ]
