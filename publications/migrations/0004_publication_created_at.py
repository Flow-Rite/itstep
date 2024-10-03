# Generated by Django 5.1.1 on 2024-10-03 10:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0003_alter_publication_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
