# Generated by Django 5.1.4 on 2025-01-06 16:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_user_alter_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='publish',
            field=models.DateField(default=datetime.datetime(2025, 1, 6, 16, 4, 44, 923737, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
