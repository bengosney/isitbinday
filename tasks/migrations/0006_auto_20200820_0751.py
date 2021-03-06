# Generated by Django 3.1 on 2020-08-20 07:51

from django.db import migrations, models
import django.utils.timezone
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_sprint_tasks'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='started',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Started'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sprint',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='state',
            field=django_fsm.FSMField(choices=[('planning', 'planning'), ('in progress', 'in progress'), ('finished', 'finished'), ('canceled', 'canceled')], default='planning', max_length=50, protected=True, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='task',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
    ]
