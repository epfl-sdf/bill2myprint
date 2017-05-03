from django.db import models


class Student(models.Model):
    sciper = models.CharField(max_length=10, db_index=True)
    section = models.ForeignKey('Section')

    def __str__(self):
        return '{}'.format(self.sciper)


class Section(models.Model):
    name = models.CharField(max_length=100, unique=True)
    acronym = models.CharField(max_length=10, unique=True)
    faculty = models.ForeignKey('Faculty')

    def __str__(self):
        return '{} : {}'.format(self.acronym, self.name)


class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return '{}'.format(self.name)


class ConsolidatedTransaction(models.Model):

    TYPE_CHOICES = (
        ('SEMESTER_ALLOWANCE', 'Allocation semestrielle'),
        ('FACULTY_ALLOWANCE', 'Rallonge facultaire'),
        ('ACCOUNT_CHARGING', "Chargement par l'étudiant"),
        ('TOTAL_SPENT', 'Total dépensé en impressions'),
    )

    transaction_type = models.CharField(max_length=100, choices=TYPE_CHOICES, db_index=True)
    amount = models.FloatField()
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
