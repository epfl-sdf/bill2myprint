from __future__ import unicode_literals

import re

from django.db import models


class Accreds(models.Model):
    sciper = models.CharField(max_length=8)
    unite = models.CharField(max_length=8)
    fonction = models.CharField(max_length=128, blank=True, null=True)
    ordre = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    statut = models.IntegerField(blank=True, null=True)
    classe = models.IntegerField(blank=True, null=True)
    datedeb = models.DateTimeField(blank=True, null=True)
    telephone1 = models.CharField(max_length=16, blank=True, null=True)
    telephone2 = models.CharField(max_length=16, blank=True, null=True)
    local = models.CharField(max_length=25, blank=True, null=True)
    comptead = models.CharField(max_length=1, blank=True, null=True)
    stockindiv = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Accreds'


class Personnes(models.Model):
    sciper = models.CharField(max_length=8, primary_key=True)
    nom = models.CharField(max_length=64, blank=True, null=True)
    prenom = models.CharField(max_length=64, blank=True, null=True)
    username = models.CharField(max_length=64, blank=True, null=True)
    home = models.CharField(max_length=64, blank=True, null=True)
    shell = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)
    physemail = models.CharField(max_length=64, blank=True, null=True)
    uid = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    adrpost = models.CharField(max_length=128, blank=True, null=True)
    cardid = models.CharField(max_length=32, blank=True, null=True)
    cardstatus = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Personnes'

    def get_full_name(self):
        return '{} {}'.format(self.nom, self.prenom)


class TStudMultipleAccredHistory(models.Model):
    sciper = models.CharField(db_column='SCIPER', max_length=8)
    new_sciper = models.CharField(db_column='NEW_SCIPER', max_length=12, blank=True, null=True)
    username = models.CharField(db_column='USERNAME', max_length=64, blank=True, null=True)
    unite_id1 = models.CharField(db_column='UNITE_ID1', max_length=50, blank=True, null=True)
    ordre1 = models.CharField(db_column='ORDRE1', max_length=64, blank=True, null=True)
    unite_id2 = models.CharField(db_column='UNITE_ID2', max_length=8, blank=True, null=True)
    ordre2 = models.CharField(db_column='ORDRE2', max_length=64, blank=True, null=True)
    unite_id3 = models.CharField(db_column='UNITE_ID3', max_length=8, blank=True, null=True)
    ordre3 = models.CharField(db_column='ORDRE3', max_length=64, blank=True, null=True)
    date_supp = models.DateTimeField(db_column='DATE_SUPP', blank=True, null=True)
    orientation = models.CharField(db_column='ORIENTATION', max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'T_STUD_MULTIPLE_ACCRED_HISTORY'


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

    class Meta:
        managed = False
        db_table = 'Unites'


class VPersonDeltaHistory(models.Model):
    person_sciper = models.CharField(db_column='PERSON_SCIPER', max_length=9, primary_key=True)
    person_lastname = models.CharField(db_column='PERSON_LASTNAME', max_length=2067, blank=True, null=True)
    person_firstname = models.CharField(db_column='PERSON_FIRSTNAME', max_length=64, blank=True, null=True)
    person_displayname = models.CharField(db_column='PERSON_DISPLAYNAME', max_length=2132, blank=True, null=True)
    person_username = models.CharField(db_column='PERSON_USERNAME', max_length=2009, blank=True, null=True)
    person_email = models.CharField(db_column='PERSON_EMAIL', max_length=64, blank=True, null=True)
    person_uid = models.IntegerField(db_column='PERSON_UID', blank=True, null=True)
    person_phone1 = models.CharField(db_column='PERSON_PHONE1', max_length=16, blank=True, null=True)
    person_phone2 = models.CharField(db_column='PERSON_PHONE2', max_length=16, blank=True, null=True)
    person_main_unit = models.CharField(db_column='PERSON_MAIN_UNIT', max_length=64, blank=True, null=True)
    person_main_unit_id = models.CharField(db_column='PERSON_MAIN_UNIT_ID', max_length=16, blank=True, null=True)
    person_position = models.CharField(db_column='PERSON_POSITION', max_length=2000, blank=True, null=True)
    person_office = models.CharField(db_column='PERSON_OFFICE', max_length=25, blank=True, null=True)
    person_gid = models.IntegerField(db_column='PERSON_GID', blank=True, null=True)
    person_dn_suffix = models.CharField(db_column='PERSON_DN_SUFFIX', max_length=2301, blank=True, null=True)
    person_cn = models.CharField(db_column='PERSON_CN', max_length=2131, blank=True, null=True)
    person_upn = models.CharField(db_column='PERSON_UPN', max_length=2200, blank=True, null=True)
    person_gone = models.CharField(db_column='PERSON_GONE', max_length=1)
    mail_enabled_address = models.CharField(db_column='MAIL_ENABLED_ADDRESS', max_length=64, blank=True, null=True)
    person_uac = models.IntegerField(db_column='PERSON_UAC')
    person_loginshell = models.CharField(db_column='PERSON_LOGINSHELL', max_length=32, blank=True, null=True)
    person_homedirectory = models.CharField(db_column='PERSON_HOMEDIRECTORY', max_length=64, blank=True, null=True)
    person_streetaddress = models.CharField(db_column='PERSON_STREETADDRESS', max_length=8000, blank=True, null=True)
    person_rfid = models.CharField(db_column='PERSON_RFID', max_length=32, blank=True, null=True)
    person_profilepath = models.CharField(db_column='PERSON_PROFILEPATH', max_length=200, blank=True, null=True)
    person_appdatapath = models.CharField(db_column='PERSON_APPDATAPATH', max_length=200, blank=True, null=True)
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)
    delta_time = models.DateTimeField(db_column='DELTA_TIME', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'V_PERSON_DELTA_HISTORY'

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


class VPersonHistory(models.Model):
    person_sciper = models.CharField(db_column='PERSON_SCIPER', max_length=9, primary_key=True)
    person_lastname = models.CharField(db_column='PERSON_LASTNAME', max_length=2067, blank=True, null=True)
    person_firstname = models.CharField(db_column='PERSON_FIRSTNAME', max_length=64, blank=True, null=True)
    person_displayname = models.CharField(db_column='PERSON_DISPLAYNAME', max_length=2132, blank=True, null=True)
    person_username = models.CharField(db_column='PERSON_USERNAME', max_length=2009, blank=True, null=True)
    person_email = models.CharField(db_column='PERSON_EMAIL', max_length=64, blank=True, null=True)
    person_uid = models.IntegerField(db_column='PERSON_UID', blank=True, null=True)
    person_phone1 = models.CharField(db_column='PERSON_PHONE1', max_length=8000, blank=True, null=True)
    person_phone2 = models.CharField(db_column='PERSON_PHONE2', max_length=16, blank=True, null=True)
    person_main_unit = models.CharField(db_column='PERSON_MAIN_UNIT', max_length=24, blank=True, null=True)
    person_main_unit_id = models.CharField(db_column='PERSON_MAIN_UNIT_ID', max_length=16, blank=True, null=True)
    person_position = models.CharField(db_column='PERSON_POSITION', max_length=2000, blank=True, null=True)
    person_office = models.CharField(db_column='PERSON_OFFICE', max_length=25, blank=True, null=True)
    person_gid = models.IntegerField(db_column='PERSON_GID', blank=True, null=True)
    person_dn_suffix = models.CharField(db_column='PERSON_DN_SUFFIX', max_length=2301, blank=True, null=True)
    person_cn = models.CharField(db_column='PERSON_CN', max_length=2131, blank=True, null=True)
    person_upn = models.CharField(db_column='PERSON_UPN', max_length=2200, blank=True, null=True)
    person_gone = models.CharField(db_column='PERSON_GONE', max_length=300, blank=True, null=True)
    mail_enabled_address = models.CharField(db_column='MAIL_ENABLED_ADDRESS', max_length=64, blank=True, null=True)
    person_uac = models.IntegerField(db_column='PERSON_UAC')
    person_loginshell = models.CharField(db_column='PERSON_LOGINSHELL', max_length=32, blank=True, null=True)
    person_homedirectory = models.CharField(db_column='PERSON_HOMEDIRECTORY', max_length=64, blank=True, null=True)
    person_streetaddress = models.CharField(db_column='PERSON_STREETADDRESS', max_length=8000, blank=True, null=True)
    person_rfid = models.CharField(db_column='PERSON_RFID', max_length=32, blank=True, null=True)
    person_profilepath = models.CharField(db_column='PERSON_PROFILEPATH', max_length=200, blank=True, null=True)
    person_appdatapath = models.CharField(db_column='PERSON_APPDATAPATH', max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'V_PERSON_HISTORY'

    def get_full_name(self):
        return '{} {}'.format(self.person_lastname, self.person_firstname)
