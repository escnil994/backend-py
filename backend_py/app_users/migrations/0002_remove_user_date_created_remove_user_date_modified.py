# Generated by Django 5.0.4 on 2024-05-04 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='user',
            name='date_modified',
        ),
    ]
