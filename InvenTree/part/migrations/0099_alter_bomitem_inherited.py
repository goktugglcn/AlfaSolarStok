# Generated by Django 3.2.18 on 2023-02-23 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0098_auto_20230214_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bomitem',
            name='inherited',
            field=models.BooleanField(default=False, help_text='This BOM item is inherited by BOMs for variant parts', verbose_name='Gets inherited'),
        ),
    ]
