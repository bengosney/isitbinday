# Generated by Django 4.1.2 on 2022-10-10 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0008_alter_ingredient_name_alter_unit_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="name",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="name",
            field=models.CharField(max_length=255, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="unit",
            name="name",
            field=models.CharField(max_length=127),
        ),
    ]
