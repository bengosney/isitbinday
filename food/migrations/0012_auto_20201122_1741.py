# Generated by Django 3.1 on 2020-11-22 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0011_auto_20201122_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='default',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='stock',
            name='quantity',
            field=models.FloatField(blank=True, default=1),
        ),
    ]