# Generated by Django 3.2.5 on 2021-11-15 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plugin', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pluginconfig',
            options={'verbose_name': 'Plugin Configuration', 'verbose_name_plural': 'Plugin Configurations'},
        ),
    ]