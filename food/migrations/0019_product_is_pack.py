# Generated by Django 3.1.4 on 2021-01-21 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0018_auto_20210112_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_pack',
            field=models.BooleanField(default=False),
        ),
    ]