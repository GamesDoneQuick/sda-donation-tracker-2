# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-08-04 20:52


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tracker", "0014_add_event_auto_approve_threshold"),
    ]

    operations = [
        migrations.AddField(
            model_name="speedrun",
            name="twitch_name",
            field=models.TextField(
                blank=True,
                help_text="What game name to use on Twitch",
                max_length=256,
                verbose_name="Twitch Name",
            ),
        ),
    ]
