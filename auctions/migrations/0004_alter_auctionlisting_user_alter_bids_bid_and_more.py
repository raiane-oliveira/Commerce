# Generated by Django 4.1.5 on 2023-01-16 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auctionlisting_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userListing', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bids',
            name='bid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100),
        ),
        migrations.AlterField(
            model_name='bids',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.auctionlisting'),
        ),
        migrations.AlterField(
            model_name='bids',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userBids', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='categories',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='auctions.auctionlisting'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='listing',
            field=models.ManyToManyField(blank=True, related_name='comments', to='auctions.auctionlisting'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]
