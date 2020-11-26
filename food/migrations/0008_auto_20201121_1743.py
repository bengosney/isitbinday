# Generated by Django 3.1 on 2020-11-21 17:43

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0007_stock_expires'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='state',
            field=django_fsm.FSMField(choices=[('In Stock', 'In Stock'), ('Consumed', 'Consumed'), ('Transferred', 'Transferred'), ('Removed', 'Removed')], default='In Stock', max_length=50, protected=True, verbose_name='State'),
        ),
        migrations.AddField(
            model_name='stock',
            name='temperature',
            field=django_fsm.FSMField(choices=[('Room Temperature', 'Room Temperature'), ('Chilled', 'Chilled'), ('Frozen', 'Frozen')], default='Room Temperature', max_length=50, protected=True, verbose_name='Temperature'),
        ),
        migrations.AlterField(
            model_name='location',
            name='temperature',
            field=models.CharField(choices=[('Room Temperature', 'Room Temperature'), ('Chilled', 'Chilled'), ('Frozen', 'Frozen')], max_length=30),
        ),
        migrations.AlterField(
            model_name='stock',
            name='quantity',
            field=models.FloatField(default=1),
        ),
    ]
