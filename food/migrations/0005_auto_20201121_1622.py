# Generated by Django 3.1 on 2020-11-21 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_auto_20201121_0820'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='type',
            new_name='temperature',
        ),
    ]
