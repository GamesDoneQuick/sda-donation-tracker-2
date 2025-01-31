# Generated by Django 5.1.4 on 2025-01-06 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0059_merge_20250129_1742'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ['event__datetime', 'speedrun__starttime', 'parent__name', 'name'], 'permissions': (('top_level_bid', 'Can create new top level bids'), ('delete_all_bids', 'Can delete bids with donations attached'), ('approve_bid', 'Can approve or deny pending bids'))},
        ),
    ]
