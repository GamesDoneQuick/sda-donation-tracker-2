# Generated by Django 4.2 on 2023-11-21 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0033_add_layout'),
    ]

    operations = [
        migrations.AddField(
            model_name='speedrun',
            name='anchor_time',
            field=models.DateTimeField(blank=True, help_text="If set, will adjust the previous run to ensure this run's start time is always this value, or throw a validation error if it is not possible", null=True),
        ),
    ]
