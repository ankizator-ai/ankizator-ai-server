# Generated by Django 5.1.4 on 2024-12-14 13:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_example_context_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='example',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.example'),
        ),
    ]