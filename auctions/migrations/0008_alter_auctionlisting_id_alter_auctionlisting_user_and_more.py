# Generated by Django 4.1.5 on 2023-01-16 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_auctionlisting_id_alter_auctionlisting_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='id',
            field=models.IntegerField(blank=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userListing', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bids',
            name='id',
            field=models.IntegerField(blank=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bids',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.auctionlisting'),
        ),
        migrations.AlterField(
            model_name='bids',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userBids', to=settings.AUTH_USER_MODEL),
        ),
    ]
