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
            name='WorkerIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker_name', models.CharField(max_length=32)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'syc_salary_worker_index',
            },
        ),
    ]