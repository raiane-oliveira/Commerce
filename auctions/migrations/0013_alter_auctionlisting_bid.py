# Generated by Django 4.1.5 on 2023-01-16 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auctionlisting_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='bid',
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
    ]
