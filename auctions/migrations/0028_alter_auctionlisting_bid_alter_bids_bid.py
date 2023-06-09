# Generated by Django 4.1.5 on 2023-01-18 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0027_alter_auctionlisting_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='bid',
            field=models.DecimalField(decimal_places=10, max_digits=100),
        ),
        migrations.AlterField(
            model_name='bids',
            name='bid',
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
    ]
