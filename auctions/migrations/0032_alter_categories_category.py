# Generated by Django 4.1.5 on 2023-01-18 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0031_alter_categories_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='category',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
