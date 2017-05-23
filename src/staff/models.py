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


class Allgraceperiodsbyunit(models.Model):
    id = models.IntegerField(primary_key=True)
    graceperiod = models.IntegerField(db_column='gracePeriod')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AllGracePeriodsByUnit'


class Classes(models.Model):
    id = models.IntegerField(primary_key=True)
    libelle = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Classes'


class Departs(models.Model):
    sciper = models.CharField(max_length=8)
    datedepart = models.DateTimeField(blank=True, null=True)
    lastunit = models.CharField(max_length=16, blank=True, null=True)
    username = models.CharField(max_length=16, blank=True, null=True)
    unithierarchie = models.CharField(db_column='UNITHIERARCHIE', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Departs'


class Droits(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    libelle = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Droits'


class Droitspersonnes(models.Model):
    droit = models.SmallIntegerField()
    sciper = models.CharField(max_length=8)
    unite = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'DroitsPersonnes'


class Graceperiodsbyunit(models.Model):
    unitid = models.IntegerField(db_column='UnitId', primary_key=True)  # Field name made lowercase.
    graceperiod = models.IntegerField(db_column='GracePeriod')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GracePeriodsByUnit'


class Groupes(models.Model):
    id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=40, blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # This field type is a guess.
    visible = models.CharField(max_length=1, blank=True, null=True)
    maillist = models.CharField(max_length=1, blank=True, null=True)
    gid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Groupes'


class Loglevels(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=450)
    order = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'LogLevels'


class Loglevelsbysource(models.Model):
    id = models.IntegerField(primary_key=True)
    source = models.CharField(unique=True, max_length=900)
    minlevel = models.ForeignKey(Loglevels, models.DO_NOTHING, db_column='minLevel')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LogLevelsBySource'


class Logs(models.Model):
    timestamp = models.DateTimeField(db_column='Timestamp')  # Field name made lowercase.
    source = models.TextField(db_column='Source', blank=True, null=True)  # Field name made lowercase.
    level = models.TextField(db_column='Level', blank=True, null=True)  # Field name made lowercase.
    message = models.TextField(db_column='Message', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Logs'


class Membres(models.Model):
    sciper = models.CharField(max_length=8, blank=True, null=True)
    groupid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Membres'


class Nortel(models.Model):
    dn = models.CharField(db_column='DN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tn = models.CharField(db_column='TN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=50, blank=True, null=True)  # Field name made lowercase.
    central = models.CharField(db_column='CENTRAL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    local = models.CharField(db_column='LOCAL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    libelle = models.CharField(db_column='LIBELLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    droit = models.CharField(db_column='DROIT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    forward_busy = models.CharField(db_column='FORWARD_BUSY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    forward_na = models.CharField(db_column='FORWARD_NA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bv = models.CharField(db_column='BV', max_length=50, blank=True, null=True)  # Field name made lowercase.
    default_forward = models.CharField(db_column='DEFAULT_FORWARD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    occurrences = models.DecimalField(db_column='OCCURRENCES', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Nortel'


class Params(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(db_column='Name')  # Field name made lowercase.
    value = models.TextField(db_column='Value', blank=True, null=True)  # Field name made lowercase.
    hierarchy = models.TextField(db_column='Hierarchy', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Params'


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


class RMembership(models.Model):
    member_id = models.CharField(db_column='MEMBER_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    group_id = models.CharField(db_column='GROUP_ID', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=6)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'R_MEMBERSHIP'


class RMembershipDelta(models.Model):
    member_id = models.CharField(db_column='MEMBER_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    group_id = models.CharField(db_column='GROUP_ID', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=6)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'R_MEMBERSHIP_DELTA'


class RMembershipDeltaHistory(models.Model):
    member_id = models.CharField(db_column='MEMBER_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    group_id = models.CharField(db_column='GROUP_ID', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=6)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    delta_time = models.DateTimeField(db_column='DELTA_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'R_MEMBERSHIP_DELTA_HISTORY'


class RMembershipHistory(models.Model):
    member_id = models.CharField(db_column='MEMBER_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    group_id = models.CharField(db_column='GROUP_ID', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=6)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'R_MEMBERSHIP_HISTORY'


class RMembershipNoDeprov(models.Model):
    member_id = models.CharField(db_column='MEMBER_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    group_id = models.CharField(db_column='GROUP_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=6)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'R_MEMBERSHIP_NO_DEPROV'


class Respads(models.Model):
    sciper = models.CharField(max_length=8)
    unite = models.IntegerField()
    valeur = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'RespADs'


class Respinfos(models.Model):
    sciper = models.CharField(max_length=8)
    unite = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'RespInfos'


class Services(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    label = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=64, blank=True, null=True)
    unit = models.CharField(max_length=8, blank=True, null=True)
    uid = models.IntegerField(blank=True, null=True)
    gid = models.IntegerField(blank=True, null=True)
    exchange = models.CharField(max_length=1, blank=True, null=True)
    camiproid = models.CharField(max_length=5, blank=True, null=True)
    camiprorfid = models.CharField(max_length=32, blank=True, null=True)
    removal = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Services'


class Statuts(models.Model):
    id = models.IntegerField(primary_key=True)
    libelle = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Statuts'


class TCadiAdUnit(models.Model):
    cadi_hierarchie = models.CharField(db_column='CADI_HIERARCHIE', max_length=300)  # Field name made lowercase.
    ad_distinguishedname = models.CharField(db_column='AD_DISTINGUISHEDNAME', max_length=300)  # Field name made lowercase.
    hierarchie_type = models.CharField(db_column='HIERARCHIE_TYPE', max_length=5)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_CADI_AD_UNIT'
        unique_together = (('cadi_hierarchie', 'ad_distinguishedname'),)


class TCadiAdUnitFirstRun(models.Model):
    cadi_hierarchie = models.CharField(db_column='CADI_HIERARCHIE', max_length=300)  # Field name made lowercase.
    ad_distinguishedname = models.CharField(db_column='AD_DISTINGUISHEDNAME', max_length=300)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_CADI_AD_UNIT_FIRST_RUN'


class TCardidPriority(models.Model):
    id_cardid_priority = models.AutoField(db_column='ID_CARDID_PRIORITY', primary_key=True)  # Field name made lowercase.
    sciper = models.CharField(db_column='SCIPER', max_length=8, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=32)  # Field name made lowercase.
    old_cardid = models.CharField(db_column='OLD_CARDID', max_length=32, blank=True, null=True)  # Field name made lowercase.
    new_cardid = models.CharField(db_column='NEW_CARDID', max_length=32, blank=True, null=True)  # Field name made lowercase.
    date_of_new = models.DateTimeField(db_column='DATE_OF_NEW')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_CARDID_PRIORITY'


class TChangelog2Notify(models.Model):
    emails = models.TextField()  # This field type is a guess.
    ou = models.TextField(db_column='OU')  # Field name made lowercase. This field type is a guess.
    log_name = models.CharField(db_column='LOG_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_CHANGELOG_2_NOTIFY'


class TGroupSuffix(models.Model):
    group_suffix_id = models.AutoField(db_column='GROUP_SUFFIX_ID', primary_key=True)  # Field name made lowercase.
    group_suffix = models.CharField(db_column='GROUP_SUFFIX', max_length=50)  # Field name made lowercase.
    group_main_unit_group = models.BooleanField(db_column='GROUP_MAIN_UNIT_GROUP')  # Field name made lowercase.
    grouptype_name = models.ForeignKey('TGroupType', models.DO_NOTHING, db_column='GROUPTYPE_NAME')  # Field name made lowercase.
    group_add_parent_as_member = models.BooleanField(db_column='GROUP_ADD_PARENT_AS_MEMBER')  # Field name made lowercase.
    group_add_child_as_member = models.BooleanField(db_column='GROUP_ADD_CHILD_AS_MEMBER')  # Field name made lowercase.
    group_dn_suffix_param_name = models.CharField(db_column='GROUP_DN_SUFFIX_PARAM_NAME', max_length=300, blank=True, null=True)  # Field name made lowercase.
    group_suffix_hierarchie_type = models.CharField(db_column='GROUP_SUFFIX_HIERARCHIE_TYPE', max_length=6)  # Field name made lowercase.
    group_deprovisioning = models.NullBooleanField(db_column='GROUP_DEPROVISIONING')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_GROUP_SUFFIX'


class TGroupType(models.Model):
    grouptype_name = models.CharField(db_column='GROUPTYPE_NAME', primary_key=True, max_length=30)  # Field name made lowercase.
    grouptype_value = models.IntegerField(db_column='GROUPTYPE_VALUE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_GROUP_TYPE'


class TLogs(models.Model):
    timestamp = models.DateTimeField(db_column='Timestamp')  # Field name made lowercase.
    source = models.TextField(db_column='Source', blank=True, null=True)  # Field name made lowercase.
    level = models.TextField(db_column='Level', blank=True, null=True)  # Field name made lowercase.
    message = models.TextField(db_column='Message', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_LOGS'


class TParam(models.Model):
    number_1 = models.AutoField(db_column='1', primary_key=True)  # Field renamed because it wasn't a valid Python identifier.
    param_name = models.CharField(db_column='PARAM_NAME', max_length=100)  # Field name made lowercase.
    param_value = models.CharField(db_column='PARAM_VALUE', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    param_hierarchie = models.CharField(db_column='PARAM_HIERARCHIE', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_PARAM'


class TPersonAccredNetprintingHistory(models.Model):
    person_sciper = models.CharField(db_column='PERSON_SCIPER', max_length=9, blank=True, null=True)  # Field name made lowercase.
    person_displayname = models.CharField(db_column='PERSON_DISPLAYNAME', max_length=129, blank=True, null=True)  # Field name made lowercase.
    person_username = models.CharField(db_column='PERSON_USERNAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_email = models.CharField(db_column='PERSON_EMAIL', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_main_unit_id = models.CharField(db_column='PERSON_MAIN_UNIT_ID', max_length=8)  # Field name made lowercase.
    person_hierarchy = models.CharField(db_column='PERSON_HIERARCHY', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    person_rfid = models.CharField(db_column='PERSON_RFID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    person_init_bal = models.CharField(db_column='PERSON_INIT_BAL', max_length=5)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_PERSON_ACCRED_NETPRINTING_HISTORY'


class TReservedNames(models.Model):
    resname_id = models.AutoField(db_column='RESNAME_ID', primary_key=True)  # Field name made lowercase.
    resname_object_name = models.CharField(db_column='RESNAME_OBJECT_NAME', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_RESERVED_NAMES'


class TStudDeptNetprintingHistory(models.Model):
    person_hierarchy = models.CharField(db_column='PERSON_HIERARCHY', max_length=8000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_STUD_DEPT_NETPRINTING_HISTORY'


class TStudMultipleAccred(models.Model):
    sciper = models.CharField(db_column='SCIPER', primary_key=True, max_length=8)  # Field name made lowercase.
    new_sciper = models.CharField(db_column='NEW_SCIPER', max_length=12, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_STUD_MULTIPLE_ACCRED'


class TStudMultipleAccredHistory(models.Model):
    sciper = models.CharField(db_column='SCIPER', max_length=8)  # Field name made lowercase.
    new_sciper = models.CharField(db_column='NEW_SCIPER', max_length=12, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unite_id1 = models.CharField(db_column='UNITE_ID1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ordre1 = models.CharField(db_column='ORDRE1', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unite_id2 = models.CharField(db_column='UNITE_ID2', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ordre2 = models.CharField(db_column='ORDRE2', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unite_id3 = models.CharField(db_column='UNITE_ID3', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ordre3 = models.CharField(db_column='ORDRE3', max_length=64, blank=True, null=True)  # Field name made lowercase.
    date_supp = models.DateTimeField(db_column='DATE_SUPP', blank=True, null=True)  # Field name made lowercase.
    orientation = models.CharField(db_column='ORIENTATION', max_length=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_STUD_MULTIPLE_ACCRED_HISTORY'


class TTempVPersonChangeUnit(models.Model):
    person_sciper = models.CharField(db_column='PERSON_SCIPER', max_length=9)  # Field name made lowercase.
    person_username = models.CharField(db_column='PERSON_USERNAME', max_length=2009)  # Field name made lowercase.
    person_dn_suffix = models.CharField(db_column='PERSON_DN_SUFFIX', max_length=2301)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16)  # Field name made lowercase.
    delta_time = models.DateTimeField(db_column='DELTA_TIME')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_TEMP_V_PERSON_CHANGE_UNIT'


class TTempVPersonChangeUnit2(models.Model):
    person_sciper = models.CharField(db_column='PERSON_SCIPER', max_length=9)  # Field name made lowercase.
    person_username = models.CharField(db_column='PERSON_USERNAME', max_length=2009)  # Field name made lowercase.
    person_dn_suffix = models.CharField(db_column='PERSON_DN_SUFFIX', max_length=2301)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16)  # Field name made lowercase.
    delta_time = models.DateTimeField(db_column='DELTA_TIME')  # Field name made lowercase.
    log_name = models.CharField(db_column='LOG_NAME', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_TEMP_V_PERSON_CHANGE_UNIT2'


class TTempVPersonEarseProfilepath(models.Model):
    person_sciper = models.CharField(db_column='PERSON_SCIPER', max_length=9)  # Field name made lowercase.
    person_username = models.CharField(db_column='PERSON_USERNAME', max_length=2009)  # Field name made lowercase.
    person_dn_suffix = models.CharField(db_column='PERSON_DN_SUFFIX', max_length=2301)  # Field name made lowercase.
    person_profilepath = models.CharField(db_column='PERSON_PROFILEPATH', max_length=200, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16)  # Field name made lowercase.
    delta_time = models.DateTimeField(db_column='DELTA_TIME')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_TEMP_V_PERSON_EARSE_PROFILEPATH'


class TUcCadiBat(models.Model):
    i_bat = models.DecimalField(db_column='I_BAT', max_digits=10, decimal_places=0)  # Field name made lowercase.
    x_abr_bat = models.CharField(db_column='X_ABR_BAT', max_length=10)  # Field name made lowercase.
    x_lib_bat = models.CharField(db_column='X_LIB_BAT', max_length=120, blank=True, null=True)  # Field name made lowercase.
    x_usuel_bat = models.CharField(db_column='X_USUEL_BAT', max_length=40, blank=True, null=True)  # Field name made lowercase.
    x_adr_rue_1 = models.CharField(db_column='X_ADR_RUE_1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    x_adr_rue_2 = models.CharField(db_column='X_ADR_RUE_2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    x_adr_np_ville = models.CharField(db_column='X_ADR_NP_VILLE', max_length=40, blank=True, null=True)  # Field name made lowercase.
    x_station = models.CharField(db_column='X_STATION', max_length=10, blank=True, null=True)  # Field name made lowercase.
    i_esp = models.DecimalField(db_column='I_ESP', max_digits=10, decimal_places=0)  # Field name made lowercase.
    x_abr_esp = models.CharField(db_column='X_ABR_ESP', max_length=20)  # Field name made lowercase.
    x_no_esp = models.CharField(db_column='X_NO_ESP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    x_usuel_esp = models.CharField(db_column='X_USUEL_ESP', max_length=40, blank=True, null=True)  # Field name made lowercase.
    x_abr_code_cus = models.CharField(db_column='X_ABR_CODE_CUS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    x_lib_sit = models.CharField(db_column='X_LIB_SIT', max_length=40)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_UC_CADI_BAT'


class TUcCadiTel(models.Model):
    i_tel_fixes = models.DecimalField(db_column='I_TEL_FIXES', max_digits=10, decimal_places=0)  # Field name made lowercase.
    x_tel = models.CharField(db_column='X_TEL', max_length=40, blank=True, null=True)  # Field name made lowercase.
    x_tel_alt = models.DecimalField(db_column='X_TEL_ALT', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    n_sciper = models.DecimalField(db_column='N_SCIPER', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    i_unite = models.DecimalField(db_column='I_UNITE', max_digits=10, decimal_places=0)  # Field name made lowercase.
    x_affichage = models.CharField(db_column='X_AFFICHAGE', max_length=240, blank=True, null=True)  # Field name made lowercase.
    i_esp = models.DecimalField(db_column='I_ESP', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    x_local = models.CharField(db_column='X_LOCAL', max_length=40, blank=True, null=True)  # Field name made lowercase.
    n_ordre = models.FloatField(db_column='N_ORDRE', blank=True, null=True)  # Field name made lowercase.
    x_attribution = models.CharField(db_column='X_ATTRIBUTION', max_length=40, blank=True, null=True)  # Field name made lowercase.
    x_modele_tel = models.CharField(db_column='X_MODELE_TEL', max_length=240, blank=True, null=True)  # Field name made lowercase.
    x_droit_sortie = models.CharField(db_column='X_DROIT_SORTIE', max_length=80, blank=True, null=True)  # Field name made lowercase.
    x_adr_machine = models.CharField(db_column='X_ADR_MACHINE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    x_remarque = models.CharField(db_column='X_REMARQUE', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    b_mobile = models.FloatField(db_column='B_MOBILE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_UC_CADI_TEL'


class TUnitNetprintingHistory(models.Model):
    unit_id = models.CharField(db_column='UNIT_ID', max_length=8)  # Field name made lowercase.
    unit_name_description = models.CharField(db_column='UNIT_NAME_DESCRIPTION', max_length=131, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_UNIT_NETPRINTING_HISTORY'


class Tablestoimport(models.Model):
    id = models.IntegerField(primary_key=True)
    isenabled = models.BooleanField(db_column='isEnabled')  # Field name made lowercase.
    cadischema = models.TextField(db_column='cadiSchema')  # Field name made lowercase.
    cadiname = models.TextField(db_column='cadiName')  # Field name made lowercase.
    staffschema = models.TextField(db_column='staffSchema')  # Field name made lowercase.
    staffname = models.TextField(db_column='staffName')  # Field name made lowercase.
    priority = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'TablesToImport'


class TempgalContacts(models.Model):
    dn = models.CharField(db_column='DN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sciper = models.CharField(max_length=10, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TempGAL_Contacts'


class Unites(models.Model):
    id = models.CharField(primary_key=True, max_length=16)
    parent = models.IntegerField(blank=True, null=True)
    sigle = models.CharField(max_length=24)
    libelle = models.CharField(max_length=128, blank=True, null=True)
    gid = models.IntegerField()
    hierarchie = models.CharField(max_length=64)
    cf = models.CharField(max_length=6, blank=True, null=True)
    du = models.DateTimeField(blank=True, null=True)
    au = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    hierarchie_parent = models.CharField(db_column='HIERARCHIE_PARENT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    parent_id = models.CharField(db_column='PARENT_ID', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Unites'


class VGroupApplicationDelta(models.Model):
    group_id = models.CharField(db_column='GROUP_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    group_name = models.CharField(db_column='GROUP_NAME', max_length=2040, blank=True, null=True)  # Field name made lowercase.
    group_description = models.CharField(db_column='GROUP_DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    group_dn_suffix = models.CharField(db_column='GROUP_DN_SUFFIX', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    group_gid = models.IntegerField(db_column='GROUP_GID', blank=True, null=True)  # Field name made lowercase.
    grouptype_value = models.IntegerField(db_column='GROUPTYPE_VALUE', blank=True, null=True)  # Field name made lowercase.
    group_email = models.CharField(db_column='GROUP_EMAIL', max_length=56, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_GROUP_APPLICATION_DELTA'


class VGroupApplicationDeltaHistory(models.Model):
    group_id = models.CharField(db_column='GROUP_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    group_name = models.CharField(db_column='GROUP_NAME', max_length=2040, blank=True, null=True)  # Field name made lowercase.
    group_description = models.CharField(db_column='GROUP_DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    group_dn_suffix = models.CharField(db_column='GROUP_DN_SUFFIX', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    group_gid = models.IntegerField(db_column='GROUP_GID', blank=True, null=True)  # Field name made lowercase.
    grouptype_value = models.IntegerField(db_column='GROUPTYPE_VALUE', blank=True, null=True)  # Field name made lowercase.
    group_email = models.CharField(db_column='GROUP_EMAIL', max_length=56, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    delta_time = models.DateTimeField(db_column='DELTA_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_GROUP_APPLICATION_DELTA_HISTORY'


class VGroupApplicationHistory(models.Model):
    group_id = models.CharField(db_column='GROUP_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    group_name = models.CharField(db_column='GROUP_NAME', max_length=2040, blank=True, null=True)  # Field name made lowercase.
    group_description = models.CharField(db_column='GROUP_DESCRIPTION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    group_dn_suffix = models.CharField(db_column='GROUP_DN_SUFFIX', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    group_gid = models.IntegerField(db_column='GROUP_GID', blank=True, null=True)  # Field name made lowercase.
    grouptype_value = models.IntegerField(db_column='GROUPTYPE_VALUE', blank=True, null=True)  # Field name made lowercase.
    group_email = models.CharField(db_column='GROUP_EMAIL', max_length=56, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_GROUP_APPLICATION_HISTORY'


class VGroupUnitDelta(models.Model):
    group_id = models.CharField(db_column='GROUP_ID', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    group_name = models.CharField(db_column='GROUP_NAME', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    group_description = models.CharField(db_column='GROUP_DESCRIPTION', max_length=128, blank=True, null=True)  # Field name made lowercase.
    group_dn_suffix = models.CharField(db_column='GROUP_DN_SUFFIX', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    group_gid = models.IntegerField(db_column='GROUP_GID', blank=True, null=True)  # Field name made lowercase.
    grouptype_value = models.IntegerField(db_column='GROUPTYPE_VALUE')  # Field name made lowercase.
    group_deprovisioning = models.NullBooleanField(db_column='GROUP_DEPROVISIONING')  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_GROUP_UNIT_DELTA'


class VGroupUnitDeltaHistory(models.Model):
    group_id = models.CharField(db_column='GROUP_ID', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    group_name = models.CharField(db_column='GROUP_NAME', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    group_description = models.CharField(db_column='GROUP_DESCRIPTION', max_length=128, blank=True, null=True)  # Field name made lowercase.
    group_dn_suffix = models.CharField(db_column='GROUP_DN_SUFFIX', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    group_gid = models.IntegerField(db_column='GROUP_GID', blank=True, null=True)  # Field name made lowercase.
    grouptype_value = models.IntegerField(db_column='GROUPTYPE_VALUE')  # Field name made lowercase.
    group_deprovisioning = models.NullBooleanField(db_column='GROUP_DEPROVISIONING')  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    delta_time = models.DateTimeField(db_column='DELTA_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_GROUP_UNIT_DELTA_HISTORY'


class VGroupUnitHistory(models.Model):
    group_id = models.CharField(db_column='GROUP_ID', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    group_name = models.CharField(db_column='GROUP_NAME', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    group_description = models.CharField(db_column='GROUP_DESCRIPTION', max_length=2064, blank=True, null=True)  # Field name made lowercase.
    group_dn_suffix = models.CharField(db_column='GROUP_DN_SUFFIX', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    group_gid = models.IntegerField(db_column='GROUP_GID', blank=True, null=True)  # Field name made lowercase.
    grouptype_value = models.IntegerField(db_column='GROUPTYPE_VALUE')  # Field name made lowercase.
    group_deprovisioning = models.NullBooleanField(db_column='GROUP_DEPROVISIONING')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_GROUP_UNIT_HISTORY'


class VPersonDelta(models.Model):
    person_sciper = models.CharField(db_column='PERSON_SCIPER', max_length=9, blank=True, null=True)  # Field name made lowercase.
    person_lastname = models.CharField(db_column='PERSON_LASTNAME', max_length=2067, blank=True, null=True)  # Field name made lowercase.
    person_firstname = models.CharField(db_column='PERSON_FIRSTNAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_displayname = models.CharField(db_column='PERSON_DISPLAYNAME', max_length=2132, blank=True, null=True)  # Field name made lowercase.
    person_username = models.CharField(db_column='PERSON_USERNAME', max_length=2009, blank=True, null=True)  # Field name made lowercase.
    person_email = models.CharField(db_column='PERSON_EMAIL', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_uid = models.IntegerField(db_column='PERSON_UID', blank=True, null=True)  # Field name made lowercase.
    person_phone1 = models.CharField(db_column='PERSON_PHONE1', max_length=16, blank=True, null=True)  # Field name made lowercase.
    person_phone2 = models.CharField(db_column='PERSON_PHONE2', max_length=16, blank=True, null=True)  # Field name made lowercase.
    person_main_unit = models.CharField(db_column='PERSON_MAIN_UNIT', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_main_unit_id = models.CharField(db_column='PERSON_MAIN_UNIT_ID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    person_position = models.CharField(db_column='PERSON_POSITION', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    person_office = models.CharField(db_column='PERSON_OFFICE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    person_gid = models.IntegerField(db_column='PERSON_GID', blank=True, null=True)  # Field name made lowercase.
    person_dn_suffix = models.CharField(db_column='PERSON_DN_SUFFIX', max_length=2301, blank=True, null=True)  # Field name made lowercase.
    person_cn = models.CharField(db_column='PERSON_CN', max_length=2131, blank=True, null=True)  # Field name made lowercase.
    person_upn = models.CharField(db_column='PERSON_UPN', max_length=2200, blank=True, null=True)  # Field name made lowercase.
    person_gone = models.CharField(db_column='PERSON_GONE', max_length=1)  # Field name made lowercase.
    mail_enabled_address = models.CharField(db_column='MAIL_ENABLED_ADDRESS', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_uac = models.IntegerField(db_column='PERSON_UAC')  # Field name made lowercase.
    person_loginshell = models.CharField(db_column='PERSON_LOGINSHELL', max_length=32, blank=True, null=True)  # Field name made lowercase.
    person_homedirectory = models.CharField(db_column='PERSON_HOMEDIRECTORY', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_streetaddress = models.CharField(db_column='PERSON_STREETADDRESS', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    person_rfid = models.CharField(db_column='PERSON_RFID', max_length=32, blank=True, null=True)  # Field name made lowercase.
    person_profilepath = models.CharField(db_column='PERSON_PROFILEPATH', max_length=200, blank=True, null=True)  # Field name made lowercase.
    person_appdatapath = models.CharField(db_column='PERSON_APPDATAPATH', max_length=200, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_PERSON_DELTA'


class VPersonDeltaHistory(models.Model):
    person_sciper = models.CharField(db_column='PERSON_SCIPER', max_length=9, primary_key=True)  # Field name made lowercase.
    person_lastname = models.CharField(db_column='PERSON_LASTNAME', max_length=2067, blank=True, null=True)  # Field name made lowercase.
    person_firstname = models.CharField(db_column='PERSON_FIRSTNAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_displayname = models.CharField(db_column='PERSON_DISPLAYNAME', max_length=2132, blank=True, null=True)  # Field name made lowercase.
    person_username = models.CharField(db_column='PERSON_USERNAME', max_length=2009, blank=True, null=True)  # Field name made lowercase.
    person_email = models.CharField(db_column='PERSON_EMAIL', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_uid = models.IntegerField(db_column='PERSON_UID', blank=True, null=True)  # Field name made lowercase.
    person_phone1 = models.CharField(db_column='PERSON_PHONE1', max_length=16, blank=True, null=True)  # Field name made lowercase.
    person_phone2 = models.CharField(db_column='PERSON_PHONE2', max_length=16, blank=True, null=True)  # Field name made lowercase.
    person_main_unit = models.CharField(db_column='PERSON_MAIN_UNIT', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_main_unit_id = models.CharField(db_column='PERSON_MAIN_UNIT_ID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    person_position = models.CharField(db_column='PERSON_POSITION', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    person_office = models.CharField(db_column='PERSON_OFFICE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    person_gid = models.IntegerField(db_column='PERSON_GID', blank=True, null=True)  # Field name made lowercase.
    person_dn_suffix = models.CharField(db_column='PERSON_DN_SUFFIX', max_length=2301, blank=True, null=True)  # Field name made lowercase.
    person_cn = models.CharField(db_column='PERSON_CN', max_length=2131, blank=True, null=True)  # Field name made lowercase.
    person_upn = models.CharField(db_column='PERSON_UPN', max_length=2200, blank=True, null=True)  # Field name made lowercase.
    person_gone = models.CharField(db_column='PERSON_GONE', max_length=1)  # Field name made lowercase.
    mail_enabled_address = models.CharField(db_column='MAIL_ENABLED_ADDRESS', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_uac = models.IntegerField(db_column='PERSON_UAC')  # Field name made lowercase.
    person_loginshell = models.CharField(db_column='PERSON_LOGINSHELL', max_length=32, blank=True, null=True)  # Field name made lowercase.
    person_homedirectory = models.CharField(db_column='PERSON_HOMEDIRECTORY', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_streetaddress = models.CharField(db_column='PERSON_STREETADDRESS', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    person_rfid = models.CharField(db_column='PERSON_RFID', max_length=32, blank=True, null=True)  # Field name made lowercase.
    person_profilepath = models.CharField(db_column='PERSON_PROFILEPATH', max_length=200, blank=True, null=True)  # Field name made lowercase.
    person_appdatapath = models.CharField(db_column='PERSON_APPDATAPATH', max_length=200, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    delta_time = models.DateTimeField(db_column='DELTA_TIME', blank=True, null=True)  # Field name made lowercase.

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


class VPersonHistory(models.Model):
    person_sciper = models.CharField(db_column='PERSON_SCIPER', max_length=9, primary_key=True)  # Field name made lowercase.
    person_lastname = models.CharField(db_column='PERSON_LASTNAME', max_length=2067, blank=True, null=True)  # Field name made lowercase.
    person_firstname = models.CharField(db_column='PERSON_FIRSTNAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_displayname = models.CharField(db_column='PERSON_DISPLAYNAME', max_length=2132, blank=True, null=True)  # Field name made lowercase.
    person_username = models.CharField(db_column='PERSON_USERNAME', max_length=2009, blank=True, null=True)  # Field name made lowercase.
    person_email = models.CharField(db_column='PERSON_EMAIL', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_uid = models.IntegerField(db_column='PERSON_UID', blank=True, null=True)  # Field name made lowercase.
    person_phone1 = models.CharField(db_column='PERSON_PHONE1', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    person_phone2 = models.CharField(db_column='PERSON_PHONE2', max_length=16, blank=True, null=True)  # Field name made lowercase.
    person_main_unit = models.CharField(db_column='PERSON_MAIN_UNIT', max_length=24, blank=True, null=True)  # Field name made lowercase.
    person_main_unit_id = models.CharField(db_column='PERSON_MAIN_UNIT_ID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    person_position = models.CharField(db_column='PERSON_POSITION', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    person_office = models.CharField(db_column='PERSON_OFFICE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    person_gid = models.IntegerField(db_column='PERSON_GID', blank=True, null=True)  # Field name made lowercase.
    person_dn_suffix = models.CharField(db_column='PERSON_DN_SUFFIX', max_length=2301, blank=True, null=True)  # Field name made lowercase.
    person_cn = models.CharField(db_column='PERSON_CN', max_length=2131, blank=True, null=True)  # Field name made lowercase.
    person_upn = models.CharField(db_column='PERSON_UPN', max_length=2200, blank=True, null=True)  # Field name made lowercase.
    person_gone = models.CharField(db_column='PERSON_GONE', max_length=300, blank=True, null=True)  # Field name made lowercase.
    mail_enabled_address = models.CharField(db_column='MAIL_ENABLED_ADDRESS', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_uac = models.IntegerField(db_column='PERSON_UAC')  # Field name made lowercase.
    person_loginshell = models.CharField(db_column='PERSON_LOGINSHELL', max_length=32, blank=True, null=True)  # Field name made lowercase.
    person_homedirectory = models.CharField(db_column='PERSON_HOMEDIRECTORY', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_streetaddress = models.CharField(db_column='PERSON_STREETADDRESS', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    person_rfid = models.CharField(db_column='PERSON_RFID', max_length=32, blank=True, null=True)  # Field name made lowercase.
    person_profilepath = models.CharField(db_column='PERSON_PROFILEPATH', max_length=200, blank=True, null=True)  # Field name made lowercase.
    person_appdatapath = models.CharField(db_column='PERSON_APPDATAPATH', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_PERSON_HISTORY'


class VSecurityPrincipalDelta(models.Model):
    group_id = models.CharField(db_column='GROUP_ID', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    secprinc_name = models.CharField(db_column='SECPRINC_NAME', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=6)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_SECURITY_PRINCIPAL_DELTA'


class VSecurityPrincipalDeltaHistory(models.Model):
    group_id = models.CharField(db_column='GROUP_ID', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    secprinc_name = models.CharField(db_column='SECPRINC_NAME', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=6)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    delta_time = models.DateTimeField(db_column='DELTA_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_SECURITY_PRINCIPAL_DELTA_HISTORY'


class VSecurityPrincipalNoDeprovDelta(models.Model):
    group_id = models.CharField(db_column='GROUP_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    secprinc_name = models.CharField(db_column='SECPRINC_NAME', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=5)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_SECURITY_PRINCIPAL_NO_DEPROV_DELTA'


class VSecurityPrincipalNoDeprovDeltaHistory(models.Model):
    group_id = models.CharField(db_column='GROUP_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    secprinc_name = models.CharField(db_column='SECPRINC_NAME', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=5)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    delta_time = models.DateTimeField(db_column='DELTA_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_SECURITY_PRINCIPAL_NO_DEPROV_DELTA_HISTORY'


class VSecurityPrincipalNoDeprovHistory(models.Model):
    group_id = models.CharField(db_column='GROUP_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    secprinc_name = models.CharField(db_column='SECPRINC_NAME', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=5)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_SECURITY_PRINCIPAL_NO_DEPROV_HISTORY'


class VStiAccred1Delta(models.Model):
    sciper = models.CharField(db_column='SCIPER', max_length=9)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    gid = models.IntegerField(db_column='GID', blank=True, null=True)  # Field name made lowercase.
    unit_id = models.CharField(db_column='UNIT_ID', max_length=8)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit_description = models.CharField(db_column='UNIT_DESCRIPTION', max_length=128, blank=True, null=True)  # Field name made lowercase.
    hierarchie = models.CharField(db_column='HIERARCHIE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_STI_ACCRED_1_DELTA'


class VStiAccred1DeltaHistory(models.Model):
    sciper = models.CharField(db_column='SCIPER', max_length=9)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    gid = models.IntegerField(db_column='GID', blank=True, null=True)  # Field name made lowercase.
    unit_id = models.CharField(db_column='UNIT_ID', max_length=8)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit_description = models.CharField(db_column='UNIT_DESCRIPTION', max_length=128, blank=True, null=True)  # Field name made lowercase.
    hierarchie = models.CharField(db_column='HIERARCHIE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    delta_time = models.DateTimeField(db_column='DELTA_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_STI_ACCRED_1_DELTA_HISTORY'


class VStiAccred1History(models.Model):
    sciper = models.CharField(db_column='SCIPER', max_length=9, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(max_length=64, blank=True, null=True)
    gid = models.IntegerField(db_column='GID', blank=True, null=True)  # Field name made lowercase.
    unit_id = models.CharField(db_column='UNIT_ID', max_length=16)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=24)  # Field name made lowercase.
    unit_description = models.CharField(db_column='UNIT_DESCRIPTION', max_length=128, blank=True, null=True)  # Field name made lowercase.
    hierarchie = models.CharField(db_column='HIERARCHIE', max_length=334, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_STI_ACCRED_1_HISTORY'


class VStiAccred1OthersDelta(models.Model):
    sciper = models.CharField(db_column='SCIPER', max_length=9)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    gid = models.IntegerField(db_column='GID', blank=True, null=True)  # Field name made lowercase.
    unit_id = models.CharField(db_column='UNIT_ID', max_length=8)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit_description = models.CharField(db_column='UNIT_DESCRIPTION', max_length=128, blank=True, null=True)  # Field name made lowercase.
    hierarchie = models.CharField(db_column='HIERARCHIE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_STI_ACCRED_1_OTHERS_DELTA'


class VStiAccred1OthersDeltaHistory(models.Model):
    sciper = models.CharField(db_column='SCIPER', max_length=9)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    gid = models.IntegerField(db_column='GID', blank=True, null=True)  # Field name made lowercase.
    unit_id = models.CharField(db_column='UNIT_ID', max_length=8)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit_description = models.CharField(db_column='UNIT_DESCRIPTION', max_length=128, blank=True, null=True)  # Field name made lowercase.
    hierarchie = models.CharField(db_column='HIERARCHIE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    delta_time = models.DateTimeField(db_column='DELTA_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_STI_ACCRED_1_OTHERS_DELTA_HISTORY'


class VStiAccred1OthersHistory(models.Model):
    sciper = models.CharField(db_column='SCIPER', max_length=9, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    gid = models.IntegerField(db_column='GID', blank=True, null=True)  # Field name made lowercase.
    unit_id = models.CharField(db_column='UNIT_ID', max_length=16)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=24)  # Field name made lowercase.
    unit_description = models.CharField(db_column='UNIT_DESCRIPTION', max_length=128, blank=True, null=True)  # Field name made lowercase.
    hierarchie = models.CharField(db_column='HIERARCHIE', max_length=334, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_STI_ACCRED_1_OTHERS_HISTORY'


class VStiAccredXDelta(models.Model):
    sciper = models.CharField(db_column='SCIPER', max_length=9)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit_id = models.CharField(db_column='UNIT_ID', max_length=8)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit_description = models.CharField(db_column='UNIT_DESCRIPTION', max_length=128, blank=True, null=True)  # Field name made lowercase.
    hierarchie = models.CharField(db_column='HIERARCHIE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_STI_ACCRED_X_DELTA'


class VStiAccredXDeltaHistory(models.Model):
    sciper = models.CharField(db_column='SCIPER', max_length=9)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit_id = models.CharField(db_column='UNIT_ID', max_length=8)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit_description = models.CharField(db_column='UNIT_DESCRIPTION', max_length=128, blank=True, null=True)  # Field name made lowercase.
    hierarchie = models.CharField(db_column='HIERARCHIE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    delta_time = models.DateTimeField(db_column='DELTA_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_STI_ACCRED_X_DELTA_HISTORY'


class VStiAccredXHistory(models.Model):
    sciper = models.CharField(db_column='SCIPER', max_length=9, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(max_length=64, blank=True, null=True)
    unit_id = models.CharField(db_column='UNIT_ID', max_length=16)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=24)  # Field name made lowercase.
    unit_description = models.CharField(db_column='UNIT_DESCRIPTION', max_length=128, blank=True, null=True)  # Field name made lowercase.
    hierarchie = models.CharField(db_column='HIERARCHIE', max_length=334, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_STI_ACCRED_X_HISTORY'


class VStiUnitsDelta(models.Model):
    unit_id = models.CharField(db_column='UNIT_ID', max_length=8)  # Field name made lowercase.
    unit_name = models.CharField(db_column='UNIT_NAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit_description = models.CharField(db_column='UNIT_DESCRIPTION', max_length=128, blank=True, null=True)  # Field name made lowercase.
    unit_gid = models.CharField(db_column='UNIT_GID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    unit_hierarchie = models.CharField(db_column='UNIT_HIERARCHIE', max_length=64, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_STI_UNITS_DELTA'


class VStiUnitsDeltaHistory(models.Model):
    unit_id = models.CharField(db_column='UNIT_ID', max_length=8)  # Field name made lowercase.
    unit_name = models.CharField(db_column='UNIT_NAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit_description = models.CharField(db_column='UNIT_DESCRIPTION', max_length=128, blank=True, null=True)  # Field name made lowercase.
    unit_gid = models.CharField(db_column='UNIT_GID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    unit_hierarchie = models.CharField(db_column='UNIT_HIERARCHIE', max_length=64, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    delta_time = models.DateTimeField(db_column='DELTA_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_STI_UNITS_DELTA_HISTORY'


class VStiUnitsHistory(models.Model):
    unit_id = models.CharField(db_column='UNIT_ID', max_length=16)  # Field name made lowercase.
    unit_name = models.CharField(db_column='UNIT_NAME', max_length=24)  # Field name made lowercase.
    unit_description = models.CharField(db_column='UNIT_DESCRIPTION', max_length=128, blank=True, null=True)  # Field name made lowercase.
    unit_gid = models.IntegerField(db_column='UNIT_GID', blank=True, null=True)  # Field name made lowercase.
    unit_hierarchie = models.CharField(db_column='UNIT_HIERARCHIE', max_length=8000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_STI_UNITS_HISTORY'


class VStokindivDelta(models.Model):
    sciper = models.CharField(max_length=8)
    username = models.CharField(db_column='USERNAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    statut = models.IntegerField(blank=True, null=True)
    unite = models.CharField(max_length=8)
    upn = models.CharField(db_column='UPN', max_length=200, blank=True, null=True)  # Field name made lowercase.
    nb_fileserver = models.CharField(max_length=1, blank=True, null=True)
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_STOKINDIV_DELTA'


class VStokindivDeltaHistory(models.Model):
    sciper = models.CharField(max_length=8)
    username = models.CharField(db_column='USERNAME', max_length=64, blank=True, null=True)  # Field name made lowercase.
    statut = models.IntegerField(blank=True, null=True)
    unite = models.CharField(max_length=8)
    upn = models.CharField(db_column='UPN', max_length=200, blank=True, null=True)  # Field name made lowercase.
    nb_fileserver = models.CharField(max_length=1, blank=True, null=True)
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    delta_time = models.DateTimeField(db_column='DELTA_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_STOKINDIV_DELTA_HISTORY'


class VStokindivHistory(models.Model):
    sciper = models.CharField(max_length=8)
    username = models.CharField(max_length=64, blank=True, null=True)
    statut = models.IntegerField(blank=True, null=True)
    unite = models.CharField(max_length=8)
    upn = models.CharField(db_column='UPN', max_length=200, blank=True, null=True)  # Field name made lowercase.
    nb_fileserver = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'V_STOKINDIV_HISTORY'


class VUnitByHierarchyDelta(models.Model):
    unit_ad_distinguishedname = models.CharField(db_column='UNIT_AD_DISTINGUISHEDNAME', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    unit_id = models.IntegerField(db_column='UNIT_ID', blank=True, null=True)  # Field name made lowercase.
    unit_name = models.CharField(db_column='UNIT_NAME', max_length=77, blank=True, null=True)  # Field name made lowercase.
    unit_description = models.CharField(db_column='UNIT_DESCRIPTION', max_length=141, blank=True, null=True)  # Field name made lowercase.
    unit_gid = models.IntegerField(db_column='UNIT_GID', blank=True, null=True)  # Field name made lowercase.
    unit_hierarchy = models.CharField(db_column='UNIT_HIERARCHY', max_length=67, blank=True, null=True)  # Field name made lowercase.
    unit_start_date = models.DateTimeField(db_column='UNIT_START_DATE', blank=True, null=True)  # Field name made lowercase.
    unit_end_date = models.DateTimeField(db_column='UNIT_END_DATE', blank=True, null=True)  # Field name made lowercase.
    hierarchie = models.CharField(db_column='HIERARCHIE', max_length=64, blank=True, null=True)  # Field name made lowercase.
    parent_hierarchy = models.CharField(db_column='PARENT_HIERARCHY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_UNIT_BY_HIERARCHY_DELTA'


class VUnitByHierarchyDeltaHistory(models.Model):
    unit_ad_distinguishedname = models.CharField(db_column='UNIT_AD_DISTINGUISHEDNAME', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    unit_id = models.IntegerField(db_column='UNIT_ID', blank=True, null=True)  # Field name made lowercase.
    unit_name = models.CharField(db_column='UNIT_NAME', max_length=77, blank=True, null=True)  # Field name made lowercase.
    unit_description = models.CharField(db_column='UNIT_DESCRIPTION', max_length=141, blank=True, null=True)  # Field name made lowercase.
    unit_gid = models.IntegerField(db_column='UNIT_GID', blank=True, null=True)  # Field name made lowercase.
    unit_hierarchy = models.CharField(db_column='UNIT_HIERARCHY', max_length=67, blank=True, null=True)  # Field name made lowercase.
    unit_start_date = models.DateTimeField(db_column='UNIT_START_DATE', blank=True, null=True)  # Field name made lowercase.
    unit_end_date = models.DateTimeField(db_column='UNIT_END_DATE', blank=True, null=True)  # Field name made lowercase.
    hierarchie = models.CharField(db_column='HIERARCHIE', max_length=64, blank=True, null=True)  # Field name made lowercase.
    parent_hierarchy = models.CharField(db_column='PARENT_HIERARCHY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    delta_time = models.DateTimeField(db_column='DELTA_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_UNIT_BY_HIERARCHY_DELTA_HISTORY'


class VUnitByHierarchyHistory(models.Model):
    unit_ad_distinguishedname = models.CharField(db_column='UNIT_AD_DISTINGUISHEDNAME', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    unit_id = models.IntegerField(db_column='UNIT_ID', blank=True, null=True)  # Field name made lowercase.
    unit_name = models.CharField(db_column='UNIT_NAME', max_length=37)  # Field name made lowercase.
    unit_description = models.CharField(db_column='UNIT_DESCRIPTION', max_length=141, blank=True, null=True)  # Field name made lowercase.
    unit_gid = models.IntegerField(db_column='UNIT_GID', blank=True, null=True)  # Field name made lowercase.
    unit_hierarchy = models.CharField(db_column='UNIT_HIERARCHY', max_length=67)  # Field name made lowercase.
    unit_start_date = models.DateTimeField(db_column='UNIT_START_DATE', blank=True, null=True)  # Field name made lowercase.
    unit_end_date = models.DateTimeField(db_column='UNIT_END_DATE', blank=True, null=True)  # Field name made lowercase.
    hierarchie = models.CharField(db_column='HIERARCHIE', max_length=64)  # Field name made lowercase.
    parent_hierarchy = models.CharField(db_column='PARENT_HIERARCHY', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_UNIT_BY_HIERARCHY_HISTORY'


class VUnitNetprintingDelta(models.Model):
    unit_id = models.CharField(db_column='UNIT_ID', max_length=8)  # Field name made lowercase.
    cf = models.CharField(db_column='CF', max_length=6, blank=True, null=True)  # Field name made lowercase.
    unit_name_description = models.CharField(db_column='UNIT_NAME_DESCRIPTION', max_length=195, blank=True, null=True)  # Field name made lowercase.
    unit_hierarchy1 = models.CharField(db_column='UNIT_HIERARCHY1', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit_hierarchy2 = models.CharField(db_column='UNIT_HIERARCHY2', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit_hierarchy3 = models.CharField(db_column='UNIT_HIERARCHY3', max_length=64, blank=True, null=True)  # Field name made lowercase.
    hierarchy1_no_display = models.CharField(db_column='HIERARCHY1_NO_DISPLAY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    hierarchy2_no_display = models.CharField(db_column='HIERARCHY2_NO_DISPLAY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    hierarchy3_no_display = models.CharField(db_column='HIERARCHY3_NO_DISPLAY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    unit_hierarchy = models.CharField(db_column='UNIT_HIERARCHY', max_length=300, blank=True, null=True)  # Field name made lowercase.
    unit_parent_hierarchy = models.CharField(db_column='UNIT_PARENT_HIERARCHY', max_length=300, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_UNIT_NETPRINTING_DELTA'


class VUnitNetprintingDeltaHistory(models.Model):
    unit_id = models.CharField(db_column='UNIT_ID', max_length=8)  # Field name made lowercase.
    cf = models.CharField(db_column='CF', max_length=6, blank=True, null=True)  # Field name made lowercase.
    unit_name_description = models.CharField(db_column='UNIT_NAME_DESCRIPTION', max_length=195, blank=True, null=True)  # Field name made lowercase.
    unit_hierarchy1 = models.CharField(db_column='UNIT_HIERARCHY1', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit_hierarchy2 = models.CharField(db_column='UNIT_HIERARCHY2', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit_hierarchy3 = models.CharField(db_column='UNIT_HIERARCHY3', max_length=64, blank=True, null=True)  # Field name made lowercase.
    hierarchy1_no_display = models.CharField(db_column='HIERARCHY1_NO_DISPLAY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    hierarchy2_no_display = models.CharField(db_column='HIERARCHY2_NO_DISPLAY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    hierarchy3_no_display = models.CharField(db_column='HIERARCHY3_NO_DISPLAY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    unit_hierarchy = models.CharField(db_column='UNIT_HIERARCHY', max_length=300, blank=True, null=True)  # Field name made lowercase.
    unit_parent_hierarchy = models.CharField(db_column='UNIT_PARENT_HIERARCHY', max_length=300, blank=True, null=True)  # Field name made lowercase.
    delta_op = models.CharField(db_column='DELTA_OP', max_length=16, blank=True, null=True)  # Field name made lowercase.
    delta_time = models.DateTimeField(db_column='DELTA_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_UNIT_NETPRINTING_DELTA_HISTORY'


class VUnitNetprintingHistory(models.Model):
    unit_id = models.CharField(db_column='UNIT_ID', max_length=16)  # Field name made lowercase.
    cf = models.CharField(db_column='CF', max_length=6, blank=True, null=True)  # Field name made lowercase.
    unit_name_description = models.CharField(db_column='UNIT_NAME_DESCRIPTION', max_length=155, blank=True, null=True)  # Field name made lowercase.
    unit_hierarchy1 = models.CharField(db_column='UNIT_HIERARCHY1', max_length=24, blank=True, null=True)  # Field name made lowercase.
    unit_hierarchy2 = models.CharField(db_column='UNIT_HIERARCHY2', max_length=24, blank=True, null=True)  # Field name made lowercase.
    unit_hierarchy3 = models.CharField(db_column='UNIT_HIERARCHY3', max_length=24, blank=True, null=True)  # Field name made lowercase.
    hierarchy1_no_display = models.CharField(db_column='HIERARCHY1_NO_DISPLAY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    hierarchy2_no_display = models.CharField(db_column='HIERARCHY2_NO_DISPLAY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    hierarchy3_no_display = models.CharField(db_column='HIERARCHY3_NO_DISPLAY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    unit_hierarchy = models.CharField(db_column='UNIT_HIERARCHY', max_length=64)  # Field name made lowercase.
    unit_parent_hierarchy = models.CharField(db_column='UNIT_PARENT_HIERARCHY', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'V_UNIT_NETPRINTING_HISTORY'


class AllEmployeeidAd(models.Model):
    dn = models.TextField(db_column='DN')  # Field name made lowercase.
    sciper = models.CharField(max_length=10, blank=True, null=True)
    username = models.CharField(max_length=20, blank=True, null=True)
    domaine = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '_ALL_EmployeeID_AD'


class Tmp(models.Model):
    member_id = models.CharField(db_column='MEMBER_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    group_id = models.CharField(db_column='GROUP_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    object_type = models.CharField(db_column='OBJECT_TYPE', max_length=6)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '_tmp'


class Lastupdates(models.Model):
    type = models.CharField(max_length=16, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lastupdates'


class Photos(models.Model):
    sciper = models.CharField(primary_key=True, max_length=8)
    photo = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'photos'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128)
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)


class TempLv(models.Model):
    sciper = models.CharField(max_length=8)
    telephone1 = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'temp_lv'
