# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-04 15:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetSemester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_spent', models.FloatField(default=0)),
                ('end_semester_budget', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('acronym', models.CharField(max_length=10, unique=True)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill2myprint.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('end_date', models.DateTimeField()),
                ('end_date_official', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sciper', models.CharField(db_index=True, max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('MYPRINT_ALLOWANCE', 'Allocation semestrielle'), ('FACULTY_ALLOWANCE', 'Rallonge facultaire'), ('ACCOUNT_CHARGING', "Chargement par l'étudiant"), ('PRINT_JOB', "Travail d'impression")], db_index=True, max_length=100)),
                ('transaction_date', models.DateTimeField()),
                ('amount', models.FloatField()),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill2myprint.Section')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill2myprint.Semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill2myprint.Student')),
            ],
        ),
        migrations.AddField(
            model_name='budgetsemester',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill2myprint.Section'),
        ),
        migrations.AddField(
            model_name='budgetsemester',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill2myprint.Semester'),
        ),
        migrations.AddField(
            model_name='budgetsemester',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bill2myprint.Student'),
        ),
    ]
