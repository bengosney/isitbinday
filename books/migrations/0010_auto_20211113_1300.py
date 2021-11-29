# Generated by Django 3.2.9 on 2021-11-13 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_auto_20211113_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='tmp_cover',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(related_name='books', to='books.Author'),
        ),
    ]