# -*- coding:utf-8 -*-

"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""

import re
from django.db import models


class Student(models.Model):
    sciper = models.CharField(max_length=10, db_index=True, blank=True)
    username = models.CharField(max_length=100, blank=True, db_index=True)
    name = models.CharField(max_length=255, blank=True, db_index=True, default='')
    has_uniflow_initial_allowance = models.BooleanField(default=False)
    last_known_section = models.ForeignKey('Section', blank=True, null=True)

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

    transaction_type = models.CharField(max_length=100, choices=TYPE_CHOICES, db_index=True)
    transaction_date = models.DateTimeField()
    semester = models.ForeignKey('Semester')
    amount = models.FloatField()
    student = models.ForeignKey('Student')
    section = models.ForeignKey('Section')
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
    billing_faculty = models.TextField(default='')
    remain = models.FloatField(default=0)

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


#class OurTAllTransactions(models.Model):
#    trans_id = models.IntegerField(db_column='TRANS_ID')
#    trans_origin = models.CharField(db_column='TRANS_ORIGIN', max_length=20, db_index=True)
#    trans_amount = models.FloatField(db_column='TRANS_AMOUNT')
#    trans_description = models.CharField(db_column='TRANS_DESCRIPTION', max_length=94, blank=True, null=True)
#    trans_source = models.CharField(db_column='TRANS_SOURCE', max_length=50, blank=True, null=True)
#    person_sciper = models.CharField(db_column='PERSON_SCIPER', max_length=10, blank=True, null=True, db_index=True)
#    account_name = models.CharField(max_length=255, blank=True, null=True)
#    trans_datetime = models.DateTimeField(db_column='TRANS_DATETIME', db_index=True)
#    trxdateonly = models.DateTimeField(blank=True, null=True)
#    trxyear = models.IntegerField(blank=True, null=True)
#    trxmonth = models.IntegerField(blank=True, null=True)
#    trxweek = models.IntegerField(blank=True, null=True)
#    trxday = models.IntegerField(blank=True, null=True)
#    trxwday = models.IntegerField(blank=True, null=True)
#    trxhourdec = models.FloatField(blank=True, null=True)
#    trx_physical_device_name = models.CharField(max_length=255, blank=True, null=True)
#    trx_docname = models.CharField(max_length=300, blank=True, null=True)
#    trx_numcopies = models.IntegerField(blank=True, null=True)
#    trx_page_count = models.IntegerField(blank=True, null=True)
#    trx_streamsize = models.IntegerField(blank=True, null=True)
#    trx_colored = models.IntegerField(blank=True, null=True)
#    trx_bw_page_count = models.IntegerField(blank=True, null=True)
#    trx_color_page_count = models.IntegerField(blank=True, null=True)
#    trx_duplex_page_count = models.IntegerField(blank=True, null=True)
#    trx_a6_page_count = models.IntegerField(blank=True, null=True)
#    trx_a5_page_count = models.IntegerField(blank=True, null=True)
#    trx_a4_page_count = models.IntegerField(blank=True, null=True)
#    trx_a3_page_count = models.IntegerField(blank=True, null=True)
#    trx_a2_page_count = models.IntegerField(blank=True, null=True)
#    trx_a1_page_count = models.IntegerField(blank=True, null=True)
#    trx_a0_page_count = models.IntegerField(blank=True, null=True)
#    trx_letter_page_count = models.IntegerField(blank=True, null=True)
#    trx_legal_page_count = models.IntegerField(blank=True, null=True)
#    trx_a6_sheet_count = models.IntegerField(blank=True, null=True)
#    trx_a5_sheet_count = models.IntegerField(blank=True, null=True)
#    trx_a4_sheet_count = models.IntegerField(blank=True, null=True)
#    trx_a3_sheet_count = models.IntegerField(blank=True, null=True)
#    trx_a2_sheet_count = models.IntegerField(blank=True, null=True)
#    trx_a1_sheet_count = models.IntegerField(blank=True, null=True)
#    trx_a0_sheet_count = models.IntegerField(blank=True, null=True)
#    trx_letter_sheet_count = models.IntegerField(blank=True, null=True)
#    trx_legal_sheet_count = models.IntegerField(blank=True, null=True)
#    trx_pagesets_summary = models.CharField(max_length=4000, blank=True, null=True)
#    user_unit_id = models.IntegerField(db_column='USER_UNIT_ID', blank=True, null=True)
#    cf = models.CharField(max_length=6, blank=True, null=True)
#    user_last_name = models.CharField(max_length=255, blank=True, null=True)
#    user_first_name = models.CharField(max_length=255, blank=True, null=True)
#    hierarchie2 = models.CharField(max_length=300, blank=True, null=True)
#    hierarchie3 = models.CharField(max_length=300, blank=True, null=True)
#    hierarchie4 = models.CharField(max_length=300, blank=True, null=True)
#    user_class = models.IntegerField(blank=True, null=True)
#
#    class Meta:
#        unique_together = (('trans_id', 'trans_origin'),)


class OurCatTransaction(models.Model):
    id = models.IntegerField(primary_key=True)
    trxtype = models.CharField(max_length=3)
    trxsubtype = models.CharField(max_length=3, blank=True, null=True)
    devid = models.IntegerField(blank=True, null=True)
    subdeviceid = models.IntegerField(blank=True, null=True)
    chargeid = models.IntegerField(blank=True, null=True)
    accountid = models.IntegerField(blank=True, null=True)
    ct1accountid = models.IntegerField(blank=True, null=True)
    ct2accountid = models.IntegerField(blank=True, null=True)
    trxdate = models.DateTimeField(db_index=True)
    creation = models.DateTimeField()
    lastmodified = models.DateTimeField()
    amount = models.DecimalField(max_digits=20, decimal_places=5)
    internalamount = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    chargeaccbalance = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    plid = models.IntegerField(blank=True, null=True)
    internalplid = models.IntegerField(blank=True, null=True)
    refid = models.IntegerField(blank=True, null=True)
    valexception = models.TextField(blank=True, null=True)
    trxstate = models.SmallIntegerField()
    applicationname = models.CharField(max_length=255, blank=True, null=True)
    trxguid = models.CharField(unique=True, max_length=64)
    approvedbyid = models.IntegerField(blank=True, null=True)
    freemoneybalance = models.DecimalField(max_digits=20, decimal_places=5)
    freemoneyamount = models.DecimalField(max_digits=20, decimal_places=5)
    grouptrxguid = models.CharField(max_length=64)


class Unites(models.Model):
    id = models.IntegerField(primary_key=True)
    parent = models.IntegerField(blank=True, null=True)
    sigle = models.CharField(max_length=24)
    libelle = models.CharField(max_length=128, blank=True, null=True)
    gid = models.IntegerField()
    hierarchie = models.CharField(max_length=64)
    cf = models.CharField(max_length=6, blank=True, null=True)
    du = models.DateTimeField(blank=True, null=True)
    au = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    hierarchie_parent = models.CharField(db_column='HIERARCHIE_PARENT', max_length=100, blank=True, null=True)
    parent_id = models.CharField(db_column='PARENT_ID', max_length=5, blank=True, null=True)


class VPersonDeltaHistory(models.Model):
    person_sciper = models.CharField(db_column='PERSON_SCIPER', max_length=9)
    person_lastname = models.CharField(db_column='PERSON_LASTNAME', max_length=2067, blank=True, null=True)
    person_firstname = models.CharField(db_column='PERSON_FIRSTNAME', max_length=64, blank=True, null=True)
    person_displayname = models.CharField(db_column='PERSON_DISPLAYNAME', max_length=2132, blank=True, null=True)
    person_username = models.CharField(db_column='PERSON_USERNAME', max_length=2009, blank=True, null=True)
    person_main_unit = models.CharField(db_column='PERSON_MAIN_UNIT', max_length=64, blank=True, null=True)
    person_main_unit_id = models.CharField(db_column='PERSON_MAIN_UNIT_ID', max_length=16, blank=True, null=True)
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)
    delta_time = models.DateTimeField(db_column='DELTA_TIME', blank=True, null=True)

    @classmethod
    def get_infos_for_equitrac(cls, username, time):
        objs = cls.objects.filter(person_username=username, delta_time__lte=time).order_by('-delta_time')
        if objs.count() == 0:
            objs = cls.objects.filter(person_username=username, delta_time__gte=time).order_by('delta_time')
            if objs.count() == 0:
                return None
        obj = objs[0]
        infos = {}
        infos['sciper'] = objs[0].person_sciper
        regex = re.search('(.*)-.*', obj.person_main_unit)
        acronym = None
        if regex:
            acronym = regex.group(1)
        if acronym:
            infos['section_acronym'] = acronym
        else:
            return None
        main_unit_id = obj.person_main_unit_id
        try:
            unit = Unites.objects.get(id=main_unit_id)
            if 'EPFL ETU' in unit.hierarchie:
                infos['is_student'] = True
            else:
                infos['is_student'] = False
        except Unites.DoesNotExist:
            infos['is_student'] = False
        return infos

    @classmethod
    def get_sciper_at_time(cls, username, time):
        objs = cls.objects.filter(person_username=username, delta_time__lte=time).order_by('-delta_time')
        if objs.count() == 0:
            return None
        return objs[0].person_sciper

    @classmethod
    def get_section_acronym_at_time(cls, sciper, time):
        acronym = ''
        objs = cls.objects.filter(person_sciper=sciper, delta_time__lte=time).order_by('-delta_time')
        if objs.count() == 0:
            return acronym
        obj = objs[0]
        regex = re.search('(.*)-.*', obj.person_main_unit)
        if regex:
            acronym = regex.group(1)
        return acronym

    @classmethod
    def get_username_at_time(cls, sciper, time):
        objs = cls.objects.filter(person_sciper=sciper, delta_time__lte=time).order_by('-delta_time')
        if objs.count() == 0:
            return ''
        return objs[0].person_username

    @classmethod
    def get_name_at_time(cls, sciper, time):
        objs = cls.objects.filter(person_sciper=sciper, delta_time__lte=time).order_by('-delta_time')
        if objs.count() == 0:
            return ''
        return '{} {}'.format(objs[0].person_lastname, objs[0].person_firstname)

    @classmethod
    def is_student_at_time(cls, sciper, time):
        objs = cls.objects.filter(person_sciper=sciper, delta_time__lte=time).order_by('-delta_time')
        if objs.count() == 0:
            return False
        person = objs[0]
        main_unit_id = person.person_main_unit_id
        try:
            unit = Unites.objects.get(id=main_unit_id)
        except Unites.DoesNotExist:
            return False
        if 'EPFL ETU' in unit.hierarchie:
            return True
        return False


class OurCatValidation(models.Model):
    id = models.IntegerField(primary_key=True)
    valtype = models.CharField(max_length=3)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    pid = models.IntegerField()
    balance = models.DecimalField(max_digits=20, decimal_places=5)
    hardlimit = models.DecimalField(max_digits=20, decimal_places=5)
    creation = models.DateTimeField()
    lastmodified = models.DateTimeField()
    expiration = models.DateTimeField(blank=True, null=True)
    state = models.SmallIntegerField()
    primarypin = models.CharField(max_length=255, blank=True, null=True)
    secondarypin = models.CharField(max_length=255, blank=True, null=True)
    parid = models.IntegerField()
    locationid = models.IntegerField(blank=True, null=True)
    nonbillable = models.SmallIntegerField(blank=True, null=True)
    freemoney = models.DecimalField(max_digits=20, decimal_places=5)

    class Meta:
        unique_together = (('valtype', 'name', 'pid', 'expiration', 'parid'),)


class CasTrxAccExt(models.Model):
    x_id = models.IntegerField(primary_key=True)
    details = models.CharField(max_length=255, blank=True, null=True)
    operatorworkstation = models.CharField(max_length=255)
    operatorname = models.CharField(max_length=255)
