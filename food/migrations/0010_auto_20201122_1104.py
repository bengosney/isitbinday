# Generated by Django 3.1 on 2020-11-22 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0009_auto_20201122_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
