# Generated by Django 4.1.5 on 2023-01-18 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0030_alter_auctionlisting_bid_alter_bids_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='category',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
