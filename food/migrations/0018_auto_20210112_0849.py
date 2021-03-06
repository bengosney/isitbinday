# Generated by Django 3.1.4 on 2021-01-12 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0017_auto_20210110_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='expires',
            field=models.DateField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='food.product'),
        ),
    ]
