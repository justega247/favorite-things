# Generated by Django 2.2.3 on 2019-07-17 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('favoriteapi', '0008_remove_historicalfavorite_modified_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalfavorite',
            name='metadata',
        ),
    ]