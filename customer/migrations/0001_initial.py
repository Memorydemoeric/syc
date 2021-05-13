# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-04-12 20:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cust_location', models.CharField(max_length=16)),
                ('cust_name', models.CharField(max_length=16)),
                ('cust_mobilephone', models.CharField(max_length=32)),
                ('cust_address', models.CharField(max_length=128)),
                ('cust_phone', models.CharField(max_length=16)),
                ('cust_rebate', models.IntegerField(default=80.0)),
                ('is_delete', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'syc_customer_info',
            },
        ),
    ]