# Generated by Django 5.1.4 on 2024-12-17 17:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_word_collection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='context',
            name='example',
        ),
        migrations.RemoveField(
            model_name='word',
            name='example',
        ),
        migrations.AddField(
            model_name='context',
            name='word',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.word'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Example',
        ),
    ]
