# Generated by Django 5.2.1 on 2025-06-17 01:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='add_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间'),
        ),
    ]
