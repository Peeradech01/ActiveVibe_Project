# Generated by Django 5.1.1 on 2024-09-26 06:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0009_remove_fitnessclass_categories_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fitnessclass',
            name='schedule',
        ),
        migrations.AddField(
            model_name='schedules',
            name='fitnessclass',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='fitness.fitnessclass'),
        ),
    ]
