# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-02-18 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_agent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='birthday',
            field=models.DateField(max_length=50, verbose_name='\u0434\u0435\u043d\u044c \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f'),
        ),
    ]