# Generated by Django 3.0.4 on 2020-03-25 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('county', '0006_auto_20200323_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('feedback', models.TextField()),
            ],
        ),
    ]
