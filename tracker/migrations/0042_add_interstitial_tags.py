# Generated by Django 5.0 on 2024-06-29 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0041_merge_0039_add_interstitial_anchor_0040_add_run_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='interstitial',
            name='tags',
            field=models.ManyToManyField(blank=True, to='tracker.runtag'),
        ),
    ]
