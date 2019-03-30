# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-18 15:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0009_auto_20190313_0815'),
        ('items', '0005_auto_20190305_1930'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_price', models.PositiveIntegerField()),
                ('description', models.CharField(max_length=512)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid', to='items.Item')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid', to='users.User')),
            ],
        ),
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='bid_item_photo/')),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemimage', to='bids.Bid')),
            ],
        ),
    ]
