# Generated by Django 3.0.4 on 2020-03-23 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('county', '0005_remove_email_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='negative_tests',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='state',
            name='positive_tests',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
