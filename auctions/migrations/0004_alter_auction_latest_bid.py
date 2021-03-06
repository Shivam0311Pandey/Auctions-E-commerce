# Generated by Django 3.2.9 on 2021-12-15 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20211214_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='latest_bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='if_bid_is_last', to='auctions.bid'),
        ),
    ]
