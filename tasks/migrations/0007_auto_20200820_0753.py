# Generated by Django 3.1 on 2020-08-20 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_auto_20200820_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='started',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Started'),
        ),
    ]
