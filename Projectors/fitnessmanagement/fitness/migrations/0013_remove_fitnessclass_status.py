# Generated by Django 5.1.1 on 2024-09-26 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0012_remove_fitnessclass_schedule_fitnessclass_end_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fitnessclass',
            name='status',
        ),
    ]
