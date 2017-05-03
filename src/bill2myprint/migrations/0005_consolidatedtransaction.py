# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-03 15:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bill2myprint', '0004_auto_20170503_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsolidatedTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('SEMESTER_ALLOWANCE', 'Allocation semestrielle'), ('FACULTY_ALLOWANCE', 'Rallonge facultaire'), ('ACCOUNT_CHARGING', "Chargement par l'étudiant"), ('TOTAL_SPENT', 'Total dépensé en impressions')], max_length=100)),
                ('amount', models.FloatField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill2myprint.Student')),
            ],
        ),
    ]
