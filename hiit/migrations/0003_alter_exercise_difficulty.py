# Generated by Django 4.0.4 on 2022-04-18 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiit', '0002_exercise_difficulty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='difficulty',
            field=models.PositiveSmallIntegerField(default=None, null=True),
        ),
    ]
