# Generated by Django 2.2.3 on 2019-07-11 17:19

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('favoriteapi', '0002_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
    ]
