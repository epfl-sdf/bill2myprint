# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-03 13:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bill2myprint', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section',
            old_name='faculte',
            new_name='faculty',
        ),
    ]
