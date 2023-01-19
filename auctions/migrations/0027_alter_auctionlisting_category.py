# Generated by Django 4.1.5 on 2023-01-17 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0026_alter_auctionlisting_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='auctions.categories'),
        ),
    ]
