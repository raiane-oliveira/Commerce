# Generated by Django 4.1.5 on 2023-01-18 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0028_alter_auctionlisting_bid_alter_bids_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='bid',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='bids',
            name='bid',
            field=models.FloatField(),
        ),
    ]