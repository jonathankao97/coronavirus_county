# Generated by Django 3.0.4 on 2020-04-02 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('county', '0009_auto_20200402_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='past_negative_tests',
            field=models.CharField(default='[]', max_length=3600),
        ),
        migrations.AddField(
            model_name='state',
            name='past_positive_tests',
            field=models.CharField(default='[]', max_length=3600),
        ),
        migrations.AddField(
            model_name='state',
            name='today_hospitalized',
            field=models.IntegerField(default=0),
        ),
    ]
