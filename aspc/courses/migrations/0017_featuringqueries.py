# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-16 22:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_auto_20160930_1656'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturingQueries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.TextField(max_length=600)),
                ('helper_text', models.TextField(max_length=300)),
            ],
        ),
    ]
