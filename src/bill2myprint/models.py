# -*- coding:utf-8 -*-

from django.db import models


class Student(models.Model):
    sciper = models.CharField(max_length=10, db_index=True, blank=True)
    username = models.CharField(max_length=100, blank=True, db_index=True)
    name = models.CharField(max_length=255, blank=True, db_index=True, default='')

    def __str__(self):
        return '{}'.format(self.sciper)


class Section(models.Model):
    name = models.CharField(max_length=100, unique=True)
    acronym = models.CharField(max_length=10, unique=True, db_index=True)
    faculty = models.ForeignKey('Faculty')

    def __str__(self):
        return '{} : {}'.format(self.acronym, self.name)


class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return '{}'.format(self.name)


class Semester(models.Model):
    name = models.CharField(max_length=255, unique=True)
    end_date = models.DateTimeField(db_index=True)
    end_date_official = models.DateTimeField()

    def __str__(self):
        return '{} : {}'.format(self.name, self.end_date.strftime('%Y-%m-%d %H:%M:%S'))


class Transaction(models.Model):

    TYPE_CHOICES = (
        ('MYPRINT_ALLOWANCE', 'Allocation semestrielle'),
        ('FACULTY_ALLOWANCE', 'Rallonge facultaire'),
        ('ACCOUNT_CHARGING', "Chargement par l'étudiant"),
        ('PRINT_JOB', "Travail d'impression"),
        ('REFUND', "Remboursement sur travail d'impression")
    )

    transaction_type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    transaction_date = models.DateTimeField()
    semester = models.ForeignKey('Semester')
    amount = models.FloatField()
    student = models.ForeignKey('Student')
    section = models.ForeignKey('Section', blank=True, null=True)
    cardinality = models.PositiveIntegerField(blank=True, default=1)
    job_type = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        out = {
            'date': self.transaction_date,
            'type': self.transaction_type,
            'semester': self.semester,
            'student': self.student,
            'section': self.section,
            'amount': self.amount
        }
        return repr(out)


class SemesterSummary(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    semester = models.ForeignKey('Semester')
    total_spent = models.FloatField(default=0)
    total_charged = models.FloatField(default=0)
    myprint_allowance = models.FloatField(default=0)
    faculty_allowance = models.FloatField(default=0)
    section = models.ForeignKey('Section')
    facturation_faculty = models.FloatField(default=0)

    class Meta:
        unique_together = ('student', 'semester', 'section')

    def __str__(self):
        out = {
                'student': self.student,
                'section': self.section,
                'semester': self.semester,
                'total_spent': self.total_spent,
                'total_charged': self.total_charged,
                'myprint_allowance': self.myprint_allowance,
                'faculty_allowance': self.faculty_allowance
                }
        return repr(out)


class UpdateStatus(models.Model):

    STATUS_CHOICES = (
        ('SUCCESS', 'Consolidation terminée avec succès'),
        ('FAILURE', 'Erreur durant la consolidation')
    )

    update_date = models.DateTimeField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    message = models.CharField(max_length=255, blank=True, default='')
