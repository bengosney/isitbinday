# Generated by Django 5.2.4 on 2025-07-03 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_alter_ingredient_name_alter_recipe_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
