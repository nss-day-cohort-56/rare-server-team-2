# Generated by Django 4.0.4 on 2022-08-15 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postreaction',
            name='user',
        ),
    ]
