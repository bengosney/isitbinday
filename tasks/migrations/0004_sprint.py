# Generated by Django 3.1 on 2020-08-20 07:37

from django.db import migrations, models
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20200820_0723'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('state', django_fsm.FSMField(choices=[('planning', 'planning'), ('in progress', 'in progress'), ('finished', 'finished')], default='planning', max_length=50, protected=True, verbose_name='State')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Created')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
            ],
        ),
    ]
