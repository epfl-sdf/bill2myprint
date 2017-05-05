from __future__ import unicode_literals

from django.db import models


class TAllTransactions(models.Model):
    trans_id = models.IntegerField(db_column='TRANS_ID', primary_key=True)  # Field name made lowercase.
    trans_origin = models.CharField(db_column='TRANS_ORIGIN', max_length=20)  # Field name made lowercase.
    trans_amount = models.FloatField(db_column='TRANS_AMOUNT')  # Field name made lowercase.
    trans_description = models.CharField(db_column='TRANS_DESCRIPTION', max_length=94, blank=True, null=True)  # Field name made lowercase.
    trans_source = models.CharField(db_column='TRANS_SOURCE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    person_sciper = models.CharField(db_column='PERSON_SCIPER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    account_name = models.CharField(max_length=255, blank=True, null=True)
    trans_datetime = models.DateTimeField(db_column='TRANS_DATETIME')  # Field name made lowercase.
    trxdateonly = models.DateTimeField(blank=True, null=True)
    trxyear = models.IntegerField(blank=True, null=True)
    trxmonth = models.IntegerField(blank=True, null=True)
    trxweek = models.IntegerField(blank=True, null=True)
    trxday = models.IntegerField(blank=True, null=True)
    trxwday = models.IntegerField(blank=True, null=True)
    trxhourdec = models.FloatField(blank=True, null=True)
    trx_physical_device_name = models.CharField(max_length=255, blank=True, null=True)
    trx_docname = models.CharField(max_length=300, blank=True, null=True)
    trx_numcopies = models.IntegerField(blank=True, null=True)
    trx_page_count = models.IntegerField(blank=True, null=True)
    trx_streamsize = models.IntegerField(blank=True, null=True)
    trx_colored = models.IntegerField(blank=True, null=True)
    trx_bw_page_count = models.IntegerField(blank=True, null=True)
    trx_color_page_count = models.IntegerField(blank=True, null=True)
    trx_duplex_page_count = models.IntegerField(blank=True, null=True)
    trx_a6_page_count = models.IntegerField(blank=True, null=True)
    trx_a5_page_count = models.IntegerField(blank=True, null=True)
    trx_a4_page_count = models.IntegerField(blank=True, null=True)
    trx_a3_page_count = models.IntegerField(blank=True, null=True)
    trx_a2_page_count = models.IntegerField(blank=True, null=True)
    trx_a1_page_count = models.IntegerField(blank=True, null=True)
    trx_a0_page_count = models.IntegerField(blank=True, null=True)
    trx_letter_page_count = models.IntegerField(blank=True, null=True)
    trx_legal_page_count = models.IntegerField(blank=True, null=True)
    trx_a6_sheet_count = models.IntegerField(blank=True, null=True)
    trx_a5_sheet_count = models.IntegerField(blank=True, null=True)
    trx_a4_sheet_count = models.IntegerField(blank=True, null=True)
    trx_a3_sheet_count = models.IntegerField(blank=True, null=True)
    trx_a2_sheet_count = models.IntegerField(blank=True, null=True)
    trx_a1_sheet_count = models.IntegerField(blank=True, null=True)
    trx_a0_sheet_count = models.IntegerField(blank=True, null=True)
    trx_letter_sheet_count = models.IntegerField(blank=True, null=True)
    trx_legal_sheet_count = models.IntegerField(blank=True, null=True)
    trx_pagesets_summary = models.CharField(max_length=4000, blank=True, null=True)
    user_unit_id = models.IntegerField(db_column='USER_UNIT_ID', blank=True, null=True)  # Field name made lowercase.
    cf = models.CharField(max_length=6, blank=True, null=True)
    user_last_name = models.CharField(max_length=255, blank=True, null=True)
    user_first_name = models.CharField(max_length=255, blank=True, null=True)
    hierarchie2 = models.CharField(max_length=300, blank=True, null=True)
    hierarchie3 = models.CharField(max_length=300, blank=True, null=True)
    hierarchie4 = models.CharField(max_length=300, blank=True, null=True)
    user_class = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'T_ALL_TRANSACTIONS'
        unique_together = (('trans_id', 'trans_origin'),)


class TSemester(models.Model):
    smst_id = models.AutoField(db_column='SMST_ID', primary_key=True)  # Field name made lowercase.
    smst_name = models.CharField(db_column='SMST_NAME', max_length=50)  # Field name made lowercase.
    smst_end_date = models.DateTimeField(db_column='SMST_END_DATE')  # Field name made lowercase.
    smst_end_date_official = models.DateTimeField(db_column='SMST_END_DATE_OFFICIAL')  # Field name made lowercase.
    smst_central_allowance_date = models.DateTimeField(db_column='SMST_CENTRAL_ALLOWANCE_DATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'T_SEMESTER'
