# Generated by Django 4.1.5 on 2023-01-17 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_alter_auctionlisting_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='listing',
        ),
        migrations.AddField(
            model_name='comments',
            name='listing',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.auctionlisting'),
        ),
    ]
