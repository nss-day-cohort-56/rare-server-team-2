# Generated by Django 4.0.4 on 2022-08-16 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0002_remove_postreaction_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='ended_on',
            field=models.DateField(null=True),
        ),
    ]
