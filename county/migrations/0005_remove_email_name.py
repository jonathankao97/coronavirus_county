# Generated by Django 3.0.4 on 2020-03-22 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('county', '0004_remove_city_city_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='name',
        ),
    ]