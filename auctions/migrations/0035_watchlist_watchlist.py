# Generated by Django 4.1.5 on 2023-01-18 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0034_remove_watchlist_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='watchlist',
            field=models.BooleanField(default=False),
        ),
    ]
