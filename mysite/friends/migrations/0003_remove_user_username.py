# Generated by Django 4.0.3 on 2022-04-03 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0002_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
