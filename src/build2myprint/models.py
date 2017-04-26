from __future__ import unicode_literals

import uuid

from django.db import models


class StringUUIDField(models.Field):
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return str(uuid.UUID(bytes_le=value)).upper()

    def to_python(self, value):
        if isinstance(value, str):
            return value

        if value is None:
            return value

        return str(uuid.UUID(bytes_le=value)).upper()


class AccesscontrollistsT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AccessControlLists_T'


class Accreds(models.Model):
    sciper = models.CharField(db_column='Sciper', max_length=6, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=32, blank=True, null=True)  # Field name made lowercase.
    cf = models.CharField(db_column='CF', max_length=6, blank=True, null=True)  # Field name made lowercase.
    hierarchie = models.CharField(db_column='Hierarchie', max_length=128, blank=True, null=True)  # Field name made lowercase.
    priceprofile = models.CharField(db_column='PriceProfile', max_length=16, blank=True, null=True)  # Field name made lowercase.
    defaultcf = models.SmallIntegerField(db_column='DefaultCF', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Accreds'


class AccredsOld(models.Model):
    sciper = models.CharField(db_column='Sciper', max_length=6, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=32, blank=True, null=True)  # Field name made lowercase.
    cf = models.CharField(db_column='CF', max_length=6, blank=True, null=True)  # Field name made lowercase.
    hierarchie = models.CharField(db_column='Hierarchie', max_length=128, blank=True, null=True)  # Field name made lowercase.
    priceprofile = models.CharField(db_column='PriceProfile', max_length=16, blank=True, null=True)  # Field name made lowercase.
    defaultcf = models.SmallIntegerField(db_column='DefaultCF', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Accreds_old'


class ActiveprintjobsT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ActivePrintJobs_T'


class AllowedcostcentersT(models.Model):
    userid = models.CharField(db_column='UserID', max_length=36)  # Field name made lowercase.
    costcenterid = models.CharField(db_column='CostCenterID', max_length=36, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AllowedCostCenters_T'


class ArchiveentryT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    jobid = models.CharField(db_column='JobID', max_length=36)  # Field name made lowercase.
    parententry = models.CharField(db_column='ParentEntry', max_length=36, blank=True, null=True)  # Field name made lowercase.
    orderinparent = models.IntegerField(db_column='OrderInParent', blank=True, null=True)  # Field name made lowercase.
    timearchived = models.DateTimeField(db_column='TimeArchived', blank=True, null=True)  # Field name made lowercase.
    timeexpiring = models.DateTimeField(db_column='TimeExpiring', blank=True, null=True)  # Field name made lowercase.
    archiveflags = models.IntegerField(db_column='ArchiveFlags', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ArchiveEntry_T'


class ArchiveindicesT(models.Model):
    indexid = models.CharField(db_column='IndexID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    indextype = models.IntegerField(db_column='IndexType')  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=100, blank=True, null=True)  # Field name made lowercase.
    archiveentry = models.CharField(db_column='ArchiveEntry', max_length=36)  # Field name made lowercase.
    parent = models.CharField(db_column='Parent', max_length=36, blank=True, null=True)  # Field name made lowercase.
    timeexpiring = models.DateTimeField(db_column='TimeExpiring', blank=True, null=True)  # Field name made lowercase.
    modified = models.DateTimeField(db_column='Modified', blank=True, null=True)  # Field name made lowercase.
    acl = models.CharField(db_column='ACL', max_length=36, blank=True, null=True)  # Field name made lowercase.
    syncflag = models.IntegerField(db_column='SyncFlag', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ArchiveIndices_T'


class ArchivedjobsT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)  # Field name made lowercase.
    cardinality = models.IntegerField(db_column='Cardinality', blank=True, null=True)  # Field name made lowercase.
    amountpaid = models.FloatField(db_column='AmountPaid', blank=True, null=True)  # Field name made lowercase.
    jobname = models.CharField(db_column='JobName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ArchivedJobs_T'


class BasystemlogT(models.Model):
    entrytime = models.DateTimeField(db_column='EntryTime')  # Field name made lowercase.
    entrytype = models.IntegerField(db_column='EntryType', blank=True, null=True)  # Field name made lowercase.
    jobid = models.CharField(db_column='JobID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=150, blank=True, null=True)  # Field name made lowercase.
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)  # Field name made lowercase.
    servername = models.CharField(db_column='ServerName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    logdata1 = models.CharField(db_column='LogData1', max_length=150, blank=True, null=True)  # Field name made lowercase.
    logdata2 = models.CharField(db_column='LogData2', max_length=150, blank=True, null=True)  # Field name made lowercase.
    entryid = models.IntegerField(db_column='EntryID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BaSystemLog_T'


class BudgettransactionsT(models.Model):
    transactiontime = models.DateTimeField(db_column='TransactionTime', primary_key=True)  # Field name made lowercase.
    transactiontype = models.IntegerField(db_column='TransactionType')  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    #entity = models.CharField(db_column='Entity', max_length=36)  # Field name made lowercase.
    entity = models.ForeignKey('ServiceconsumerT', db_column='Entity', primary_key=True)
    #service = models.CharField(db_column='Service', max_length=36, blank=True, null=True)  # Field name made lowercase.
    service = models.ForeignKey('ServiceT', db_column='Service')
    serviceusage = models.CharField(db_column='ServiceUsage', max_length=36, blank=True, null=True)  # Field name made lowercase.
    transactiondata = models.CharField(db_column='TransactionData', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BudgetTransactions_T'
        unique_together = ('entity', 'transactiontime')


class Camipro(models.Model):
    sciper = models.CharField(db_column='Sciper', max_length=6, blank=True, null=True)  # Field name made lowercase.
    cardid = models.CharField(db_column='CardId', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Camipro'


class CamiproOld(models.Model):
    sciper = models.CharField(db_column='Sciper', max_length=6, blank=True, null=True)  # Field name made lowercase.
    cardid = models.CharField(db_column='CardId', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Camipro_old'


class Centrefraisunite(models.Model):
    cf = models.CharField(db_column='CF', max_length=6, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=32, blank=True, null=True)  # Field name made lowercase.
    invoice = models.CharField(db_column='Invoice', max_length=1, blank=True, null=True)  # Field name made lowercase.
    manager = models.CharField(db_column='Manager', max_length=6, blank=True, null=True)  # Field name made lowercase.
    deputy = models.CharField(db_column='Deputy', max_length=6, blank=True, null=True)  # Field name made lowercase.
    hierarchy = models.CharField(db_column='Hierarchy', max_length=128, blank=True, null=True)  # Field name made lowercase.
    priceprofile = models.CharField(db_column='PriceProfile', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CentreFraisUnite'


class ConfigobjectsT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ConfigObjects_T'


class ConsumergrouplinksT(models.Model):
    upperlink = models.CharField(db_column='UpperLink', max_length=36)  # Field name made lowercase.
    lowerlink = models.CharField(db_column='LowerLink', max_length=36)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ConsumerGroupLinks_T'


class ConsumeridentitiesT(models.Model):
    # id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    id = StringUUIDField(db_column='ID', primary_key=True)
    classdata = models.BinaryField(db_column='ClassData')  # Field name made lowercase.
    # consumerid = models.CharField(db_column='ConsumerID', max_length=36)  # Field name made lowercase.
    consumerid = StringUUIDField(db_column='ConsumerID', primary_key=True)
    identitycategory = models.IntegerField(db_column='IdentityCategory')  # Field name made lowercase.
    identitytype = models.CharField(db_column='IdentityType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=255, blank=True, null=True)  # Field name made lowercase.
    defaultidentity = models.IntegerField(db_column='DefaultIdentity', blank=True, null=True)  # Field name made lowercase.
    visibility = models.IntegerField(db_column='Visibility', blank=True, null=True)  # Field name made lowercase.
    dispositionchecked = models.IntegerField(db_column='DispositionChecked', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ConsumerIdentities_T'


class Copernic(models.Model):
    sciper = models.CharField(db_column='Sciper', max_length=50)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=50)  # Field name made lowercase.
    cf = models.CharField(db_column='CF', max_length=50)  # Field name made lowercase.
    changetype = models.CharField(db_column='ChangeType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    priceprofile = models.CharField(db_column='PriceProfile', max_length=50)  # Field name made lowercase.
    defaultcf = models.SmallIntegerField(db_column='DefaultCF')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Copernic'


class Copernic2(models.Model):
    sciper = models.CharField(db_column='Sciper', max_length=6, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=32, blank=True, null=True)  # Field name made lowercase.
    cf = models.CharField(db_column='CF', max_length=6, blank=True, null=True)  # Field name made lowercase.
    defaultcf = models.CharField(db_column='DefaultCF', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updated = models.IntegerField(db_column='Updated')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Copernic2'


class CostsavingsT(models.Model):
    usagebegin = models.DateTimeField(db_column='UsageBegin')  # Field name made lowercase.
    usageend = models.DateTimeField(db_column='UsageEnd')  # Field name made lowercase.
    serviceproviderinput = models.CharField(db_column='ServiceProviderInput', max_length=36)  # Field name made lowercase.
    serviceprovider = models.CharField(db_column='ServiceProvider', max_length=36)  # Field name made lowercase.
    serviceconsumer = models.CharField(db_column='ServiceConsumer', max_length=36)  # Field name made lowercase.
    servconsgroup = models.CharField(db_column='ServConsGroup', max_length=36)  # Field name made lowercase.
    servconsproject = models.CharField(db_column='ServConsProject', max_length=36)  # Field name made lowercase.
    jobname = models.CharField(db_column='JobName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    formatcode = models.IntegerField(db_column='FormatCode')  # Field name made lowercase.
    pages = models.IntegerField(db_column='Pages')  # Field name made lowercase.
    pagescolor = models.IntegerField(db_column='PagesColor')  # Field name made lowercase.
    pagesduplex = models.IntegerField(db_column='PagesDuplex')  # Field name made lowercase.
    costs = models.FloatField(db_column='Costs', blank=True, null=True)  # Field name made lowercase.
    costssaved = models.FloatField(db_column='CostsSaved', blank=True, null=True)  # Field name made lowercase.
    costssavedpot = models.FloatField(db_column='CostsSavedPot', blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type')  # Field name made lowercase.
    typepot = models.IntegerField(db_column='TypePot')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CostSavings_T'


class CountercheckT(models.Model):
    serviceprovider = models.CharField(db_column='ServiceProvider', max_length=36)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='Timestamp')  # Field name made lowercase.
    servicecode = models.IntegerField(db_column='ServiceCode', blank=True, null=True)  # Field name made lowercase.
    counterorigin = models.IntegerField(db_column='CounterOrigin', blank=True, null=True)  # Field name made lowercase.
    value = models.IntegerField(db_column='Value', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CounterCheck_T'


class EventsT(models.Model):
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    device = models.CharField(db_column='Device', max_length=36)  # Field name made lowercase.
    serialnumber = models.CharField(db_column='SerialNumber', max_length=50, blank=True, null=True)  # Field name made lowercase.
    devicetype = models.IntegerField(db_column='DeviceType', blank=True, null=True)  # Field name made lowercase.
    eventtype = models.IntegerField(db_column='EventType', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    statusex = models.CharField(db_column='StatusEx', max_length=64, blank=True, null=True)  # Field name made lowercase.
    statuschange = models.CharField(db_column='StatusChange', max_length=64, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=150, blank=True, null=True)  # Field name made lowercase.
    assocentity = models.CharField(db_column='AssocEntity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    totalcounter = models.IntegerField(db_column='TotalCounter', blank=True, null=True)  # Field name made lowercase.
    manufacturerinfo = models.CharField(db_column='ManufacturerInfo', max_length=150, blank=True, null=True)  # Field name made lowercase.
    systemservername = models.CharField(db_column='SystemServerName', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Events_T'


class GroupmembershipT(models.Model):
    # userid = models.CharField(db_column='UserID', max_length=36)  # Field name made lowercase.
    # userid = StringUUIDField(db_column='UserID', primary_key=True)
    userid = models.ForeignKey('ServiceconsumerT', db_column='UserID', primary_key=True)
    # groupid = models.CharField(db_column='GroupID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    groupid = StringUUIDField(db_column='GroupID', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GroupMembership_T'
        unique_together = ('userid', 'groupid')


class MomsystemtasksT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastexecution = models.DateTimeField(db_column='LastExecution', blank=True, null=True)  # Field name made lowercase.
    nextexecution = models.DateTimeField(db_column='NextExecution', blank=True, null=True)  # Field name made lowercase.
    lastexecutionresult = models.IntegerField(db_column='LastExecutionResult', blank=True, null=True)  # Field name made lowercase.
    lasterror = models.CharField(db_column='LastError', max_length=50, blank=True, null=True)  # Field name made lowercase.
    machinename = models.CharField(db_column='MachineName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MomSystemTasks_T'


class ObjecthistoryT(models.Model):
    version = models.BigIntegerField(db_column='Version')  # Field name made lowercase.
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    parentid = models.CharField(db_column='ParentID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)  # Field name made lowercase.
    objecttype = models.CharField(db_column='ObjectType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    objectname = models.CharField(db_column='ObjectName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    modified = models.DateTimeField(db_column='Modified', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=1024, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ObjectHistory_T'


class OrderitemsT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    orderid = models.CharField(db_column='OrderID', max_length=36)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    amountpaid = models.FloatField(db_column='AmountPaid', blank=True, null=True)  # Field name made lowercase.
    copycount = models.IntegerField(db_column='CopyCount', blank=True, null=True)  # Field name made lowercase.
    vat = models.FloatField(db_column='VAT', blank=True, null=True)  # Field name made lowercase.
    pricedetailtext = models.CharField(db_column='PriceDetailText', max_length=2048, blank=True, null=True)  # Field name made lowercase.
    producttype = models.IntegerField(db_column='ProductType', blank=True, null=True)  # Field name made lowercase.
    queuename = models.CharField(db_column='QueueName', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OrderItems_T'


class OrderT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=36)  # Field name made lowercase.
    number = models.CharField(db_column='Number', max_length=50, blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    visibility = models.IntegerField(db_column='Visibility', blank=True, null=True)  # Field name made lowercase.
    cardtransaction = models.CharField(db_column='CardTransaction', max_length=36, blank=True, null=True)  # Field name made lowercase.
    paymentmethod = models.CharField(db_column='PaymentMethod', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Order_T'


class PeersT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Peers_T'


class PrintjobhistoryT(models.Model):
    jobid = models.CharField(db_column='JobID', max_length=36)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fieldname = models.CharField(db_column='FieldName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    oldvalue = models.CharField(db_column='OldValue', max_length=250, blank=True, null=True)  # Field name made lowercase.
    newvalue = models.CharField(db_column='NewValue', max_length=250, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PrintJobHistory_T'


class PrinterclusterT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    momsyncflag = models.NullBooleanField(db_column='MomSyncFlag')  # Field name made lowercase.
    clusterrole = models.IntegerField(db_column='ClusterRole', blank=True, null=True)  # Field name made lowercase.
    productfamily = models.IntegerField(db_column='ProductFamily', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PrinterCluster_T'


class Reportdata(models.Model):
    transactglobalid = models.CharField(db_column='TransactGlobalID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    jobdate = models.DateTimeField(db_column='JobDate', blank=True, null=True)  # Field name made lowercase.
    resourcetype = models.CharField(db_column='ResourceType', max_length=2)  # Field name made lowercase.
    pgecnt = models.IntegerField(db_column='PgeCnt', blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    costcoloured = models.FloatField(db_column='CostColoured', blank=True, null=True)  # Field name made lowercase.
    costbw = models.FloatField(db_column='CostBW', blank=True, null=True)  # Field name made lowercase.
    pagescoloured = models.IntegerField(db_column='PagesColoured', blank=True, null=True)  # Field name made lowercase.
    pagesbw = models.IntegerField(db_column='PagesBW', blank=True, null=True)  # Field name made lowercase.
    completepgecnt = models.IntegerField(db_column='CompletePgeCnt', blank=True, null=True)  # Field name made lowercase.
    pagesa4 = models.IntegerField(db_column='PagesA4', blank=True, null=True)  # Field name made lowercase.
    pagesa3 = models.IntegerField(db_column='PagesA3', blank=True, null=True)  # Field name made lowercase.
    pagesother = models.IntegerField(db_column='PagesOther', blank=True, null=True)  # Field name made lowercase.
    cc = models.CharField(db_column='CC', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ccdesc = models.CharField(db_column='CCDesc', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ccid = models.CharField(db_column='CCID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    invoiceflag = models.CharField(db_column='InvoiceFlag', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ReportData'


class ServiceconsumerT(models.Model):
    #id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    id = StringUUIDField(db_column='ID', primary_key=True)
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    login = models.CharField(db_column='Login', max_length=50, blank=True, null=True)  # Field name made lowercase.
    defaultgroupid = models.CharField(db_column='DefaultGroupID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    usertypeex = models.IntegerField(db_column='UserTypeEx', blank=True, null=True)  # Field name made lowercase.
    payconid = models.CharField(db_column='PayConID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    usertype = models.CharField(db_column='UserType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    addressone = models.CharField(db_column='AddressOne', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addresstwo = models.CharField(db_column='AddressTwo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    zip = models.CharField(db_column='Zip', max_length=20, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=50, blank=True, null=True)  # Field name made lowercase.
    memo = models.CharField(db_column='Memo', max_length=250, blank=True, null=True)  # Field name made lowercase.
    defaultcostcenter = models.CharField(db_column='DefaultCostCenter', max_length=36, blank=True, null=True)  # Field name made lowercase.
    hasbiodata = models.IntegerField(db_column='HasBioData', blank=True, null=True)  # Field name made lowercase.
    visibility = models.IntegerField(db_column='Visibility', blank=True, null=True)  # Field name made lowercase.
    emergencyaccountflag = models.NullBooleanField(db_column='EmergencyAccountFlag')  # Field name made lowercase.
    cslogininfo = models.CharField(db_column='CsLoginInfo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sapname = models.CharField(db_column='SAPName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pincodehash = models.CharField(db_column='PinCodeHash', max_length=80, blank=True, null=True)  # Field name made lowercase.
    momsyncflag = models.NullBooleanField(db_column='MomSyncFlag')  # Field name made lowercase.
    linkedconsumerid = models.CharField(db_column='LinkedConsumerID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    modified = models.DateTimeField(db_column='Modified', blank=True, null=True)  # Field name made lowercase.
    customprop_igstatus = models.CharField(db_column='CustomProp_IGStatus', max_length=5, blank=True, null=True)  # Field name made lowercase.
    customprop_iglogin = models.CharField(db_column='CustomProp_IGLOGIN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=10, blank=True, null=True)  # Field name made lowercase.
    hierarchyposition = models.CharField(db_column='HierarchyPosition', max_length=36, blank=True, null=True)  # Field name made lowercase.
    forcedrilldown = models.IntegerField(db_column='ForceDrillDown', blank=True, null=True)  # Field name made lowercase.
    emailaddress = models.CharField(db_column='EmailAddress', max_length=50, blank=True, null=True)  # Field name made lowercase.
    objectcontainerversion = models.IntegerField(db_column='OBJECTCONTAINERVERSION', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ServiceConsumer_T'


class ServiceproviderT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    payconserialno = models.CharField(db_column='PayConSerialNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    displayindex = models.IntegerField(db_column='DisplayIndex', blank=True, null=True)  # Field name made lowercase.
    printername = models.CharField(db_column='PrinterName', max_length=150, blank=True, null=True)  # Field name made lowercase.
    routinggroup = models.CharField(db_column='RoutingGroup', max_length=50, blank=True, null=True)  # Field name made lowercase.
    servername = models.CharField(db_column='ServerName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    payconipaddress = models.CharField(db_column='PayConIpAddress', max_length=50, blank=True, null=True)  # Field name made lowercase.
    providertype = models.IntegerField(db_column='ProviderType', blank=True, null=True)  # Field name made lowercase.
    pricingprofile = models.CharField(db_column='PricingProfile', max_length=36, blank=True, null=True)  # Field name made lowercase.
    hideprinterfromwqm = models.IntegerField(db_column='HidePrinterFromWqm', blank=True, null=True)  # Field name made lowercase.
    visibility = models.IntegerField(db_column='Visibility', blank=True, null=True)  # Field name made lowercase.
    mgmtdata_customernumber = models.CharField(db_column='MgmtData_CustomerNumber', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mgmtdata_monthlyvolume = models.CharField(db_column='MgmtData_MonthlyVolume', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mgmtdata_contractstart = models.CharField(db_column='MgmtData_ContractStart', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mgmtdata_contractend = models.CharField(db_column='MgmtData_ContractEnd', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mgmtdata_serial = models.CharField(db_column='MgmtData_Serial', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mgmtdata_location = models.CharField(db_column='MgmtData_Location', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mgmtdata_assetnumber = models.CharField(db_column='MgmtData_AssetNumber', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mgmtdata_hostname = models.CharField(db_column='MgmtData_Hostname', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mgmtdata_macaddress = models.CharField(db_column='MgmtData_MacAddress', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mgmtdata_modelname = models.CharField(db_column='MgmtData_ModelName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    momsyncflag = models.NullBooleanField(db_column='MomSyncFlag')  # Field name made lowercase.
    modified = models.DateTimeField(db_column='Modified', blank=True, null=True)  # Field name made lowercase.
    wizardname = models.CharField(db_column='WizardName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mgmtdata_manufacturer = models.CharField(db_column='MgmtData_Manufacturer', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mgmtdata_productfamily = models.CharField(db_column='MgmtData_ProductFamily', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ServiceProvider_T'


class ServiceusagecontainerinfoT(models.Model):
    jobid = models.CharField(db_column='JobID', max_length=36)  # Field name made lowercase.
    jobkey = models.CharField(db_column='JobKey', max_length=50, blank=True, null=True)  # Field name made lowercase.
    jobvalue = models.CharField(db_column='JobValue', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ServiceUsageContainerInfo_T'


class ServiceusageT(models.Model):
    #id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    id = StringUUIDField(db_column='ID', primary_key=True)
    serviceprovider = models.CharField(db_column='ServiceProvider', max_length=36)  # Field name made lowercase.
    service = models.CharField(db_column='Service', max_length=36, blank=True, null=True)  # Field name made lowercase.
    #serviceconsumer = models.CharField(db_column='ServiceConsumer', max_length=36, blank=True, null=True)  # Field name made lowercase.
    serviceconsumer = models.ForeignKey(ServiceconsumerT, db_column='ServiceConsumer')
    #servconsgroup = models.CharField(db_column='ServConsGroup', max_length=36, blank=True, null=True)  # Field name made lowercase.
    servconsgroup = models.ForeignKey(ServiceconsumerT, db_column='ServConsGroup', related_name='serviceusage_servconsgroup_set')
    #servconsproject = models.CharField(db_column='ServConsProject', max_length=36, blank=True, null=True)  # Field name made lowercase.
    servconsproject = models.ForeignKey(ServiceconsumerT, db_column='ServConsProject', related_name='serviceusage_servconsproject_set')
    cardnumber = models.IntegerField(db_column='CardNumber', blank=True, null=True)  # Field name made lowercase.
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)  # Field name made lowercase.
    usagebegin = models.DateTimeField(db_column='UsageBegin', blank=True, null=True)  # Field name made lowercase.
    usageend = models.DateTimeField(db_column='UsageEnd', blank=True, null=True)  # Field name made lowercase.
    cardinality = models.IntegerField(db_column='Cardinality', blank=True, null=True)  # Field name made lowercase.
    amountpaid = models.FloatField(db_column='AmountPaid', blank=True, null=True)  # Field name made lowercase.
    parentservice = models.CharField(db_column='ParentService', max_length=36, blank=True, null=True)  # Field name made lowercase.
    jobname = models.CharField(db_column='JobName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    streamversion = models.CharField(db_column='StreamVersion', max_length=30, blank=True, null=True)  # Field name made lowercase.
    jobticketfield = models.CharField(db_column='JobTicketField', max_length=60, blank=True, null=True)  # Field name made lowercase.
    jobticketfieldtwo = models.CharField(db_column='JobTicketFieldTwo', max_length=60, blank=True, null=True)  # Field name made lowercase.
    jobticketfieldthree = models.CharField(db_column='JobTicketFieldThree', max_length=60, blank=True, null=True)  # Field name made lowercase.
    copycount = models.IntegerField(db_column='CopyCount', blank=True, null=True)  # Field name made lowercase.
    nonchargeable = models.IntegerField(db_column='NonChargeable', blank=True, null=True)  # Field name made lowercase.
    nonchargereason = models.CharField(db_column='NonChargeReason', max_length=255, blank=True, null=True)  # Field name made lowercase.
    momsyncflag = models.NullBooleanField(db_column='MomSyncFlag')  # Field name made lowercase.
    altprice0 = models.FloatField(db_column='AltPrice0', blank=True, null=True)  # Field name made lowercase.
    altprice1 = models.FloatField(db_column='AltPrice1', blank=True, null=True)  # Field name made lowercase.
    altprice2 = models.FloatField(db_column='AltPrice2', blank=True, null=True)  # Field name made lowercase.
    costsavings = models.FloatField(db_column='CostSavings', blank=True, null=True)  # Field name made lowercase.
    cpcajobid = models.CharField(db_column='CpcaJobID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    costcenterpath = models.CharField(db_column='CostCenterPath', max_length=512, blank=True, null=True)  # Field name made lowercase.
    jobsettings_cloneof = models.CharField(db_column='JobSettings_CloneOf', max_length=38, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ServiceUsage_T'


class ServiceT(models.Model):
    #id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    id = StringUUIDField(db_column='ID', primary_key=True)
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    serviceprovider = models.CharField(db_column='ServiceProvider', max_length=36)  # Field name made lowercase.
    servicecode = models.IntegerField(db_column='ServiceCode', blank=True, null=True)  # Field name made lowercase.
    providerindex = models.IntegerField(db_column='ProviderIndex', blank=True, null=True)  # Field name made lowercase.
    visibility = models.IntegerField(db_column='Visibility', blank=True, null=True)  # Field name made lowercase.
    momsyncflag = models.NullBooleanField(db_column='MomSyncFlag')  # Field name made lowercase.
    modified = models.DateTimeField(db_column='Modified', blank=True, null=True)  # Field name made lowercase.
    acl = models.CharField(db_column='ACL', max_length=36, blank=True, null=True)  # Field name made lowercase.
    jttag = models.CharField(db_column='JtTag', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Service_T'


class SinglerowstatT(models.Model):
    entrytime = models.DateTimeField(db_column='EntryTime')  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=15, blank=True, null=True)  # Field name made lowercase.
    jobname = models.CharField(db_column='JobName', max_length=250, blank=True, null=True)  # Field name made lowercase.
    printername = models.CharField(db_column='PrinterName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    servername = models.CharField(db_column='ServerName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    formatcode = models.IntegerField(db_column='FormatCode')  # Field name made lowercase.
    totalpages = models.IntegerField(db_column='TotalPages')  # Field name made lowercase.
    duplexpages = models.IntegerField(db_column='DuplexPages')  # Field name made lowercase.
    colorpages = models.IntegerField(db_column='ColorPages')  # Field name made lowercase.
    inputtray = models.SmallIntegerField(db_column='InputTray')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SingleRowStat_T'


class VendingtransactionsT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)  # Field name made lowercase.
    classdata = models.BinaryField(db_column='ClassData')  # Field name made lowercase.
    consumerid = models.CharField(db_column='ConsumerID', max_length=36)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VendingTransactions_T'
