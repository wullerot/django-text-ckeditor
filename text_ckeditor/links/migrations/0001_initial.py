# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-14 14:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, default='', max_length=255, verbose_name='URL')),
                ('target', models.CharField(blank=True, choices=[('', 'same window'), ('_blank', 'new window')], default='', max_length=255, verbose_name='target')),
                ('email', models.EmailField(blank=True, default='', max_length=254, verbose_name='Email')),
            ],
            options={
                'managed': False,
            },
        ),
    ]