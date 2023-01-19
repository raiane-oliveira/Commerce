# Generated by Django 4.1.5 on 2023-01-17 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_alter_categories_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='listing',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='category',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='auctions.categories'),
        ),
        migrations.AlterField(
            model_name='categories',
            name='category',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
