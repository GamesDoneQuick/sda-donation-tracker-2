# Generated by Django 5.1 on 2024-09-30 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0045_merge_runner_and_headset'),
    ]

    operations = [
        migrations.RenameModel(old_name='Runner', new_name='Talent'),
        migrations.AlterModelOptions(
            name='talent',
            options={'verbose_name_plural': 'Talent'},
        ),
        migrations.AlterField(
            model_name='talent',
            name='name',
            field=models.CharField(
                error_messages={'unique': 'Talent with this case-insensitive Name already exists.'}, max_length=64,
                unique=True),
        ),
        migrations.RemoveField(model_name='speedrun', name='hosts'),
        migrations.RemoveField(model_name='speedrun', name='commentators'),
        migrations.RenameField(model_name='speedrun', old_name='thosts', new_name='hosts'),
        migrations.RenameField(model_name='speedrun', old_name='tcommentators', new_name='commentators'),
        migrations.AlterField(
            model_name='speedrun',
            name='runners',
            field=models.ManyToManyField(related_name='runs', to='tracker.talent'),
        ),
        migrations.AlterField(model_name='speedrun', name='hosts', field=
            models.ManyToManyField(blank=True, related_name='hosting', to='tracker.talent')
        ),
        migrations.AlterField(model_name='speedrun', name='commentators', field=
            models.ManyToManyField(blank=True, related_name='commentating', to='tracker.talent')
        ),
        migrations.DeleteModel(name='Headset'),
    ]
