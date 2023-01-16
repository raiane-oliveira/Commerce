# Generated by Django 4.1.5 on 2023-01-16 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_auctionlisting_id_alter_bids_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userListing', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bids',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='bids',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.auctionlisting'),
        ),
        migrations.AlterField(
            model_name='bids',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userBids', to=settings.AUTH_USER_MODEL),
        ),
    ]