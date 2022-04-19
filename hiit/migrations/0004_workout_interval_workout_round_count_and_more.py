# Generated by Django 4.0.4 on 2022-04-18 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiit', '0003_alter_exercise_difficulty'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='interval',
            field=models.DurationField(default=15),
        ),
        migrations.AddField(
            model_name='workout',
            name='round_count',
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name='workout',
            name='round_length',
            field=models.DurationField(default=42),
        ),
    ]
