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
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'AccessControlLists_T'


class Accreds(models.Model):
    sciper = models.CharField(db_column='Sciper', max_length=6, blank=True, null=True)
    unit = models.CharField(db_column='Unit', max_length=32, blank=True, null=True)
    cf = models.CharField(db_column='CF', max_length=6, blank=True, null=True)
    hierarchie = models.CharField(db_column='Hierarchie', max_length=128, blank=True, null=True)
    priceprofile = models.CharField(db_column='PriceProfile', max_length=16, blank=True, null=True)
    defaultcf = models.SmallIntegerField(db_column='DefaultCF', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Accreds'


class AccredsOld(models.Model):
    sciper = models.CharField(db_column='Sciper', max_length=6, blank=True, null=True)
    unit = models.CharField(db_column='Unit', max_length=32, blank=True, null=True)
    cf = models.CharField(db_column='CF', max_length=6, blank=True, null=True)
    hierarchie = models.CharField(db_column='Hierarchie', max_length=128, blank=True, null=True)
    priceprofile = models.CharField(db_column='PriceProfile', max_length=16, blank=True, null=True)
    defaultcf = models.SmallIntegerField(db_column='DefaultCF', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Accreds_old'


class ActiveprintjobsT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ActivePrintJobs_T'


class AllowedcostcentersT(models.Model):
    userid = models.CharField(db_column='UserID', max_length=36)
    costcenterid = models.CharField(db_column='CostCenterID', max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'AllowedCostCenters_T'


class ArchiveentryT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)
    jobid = models.CharField(db_column='JobID', max_length=36)
    parententry = models.CharField(db_column='ParentEntry', max_length=36, blank=True, null=True)
    orderinparent = models.IntegerField(db_column='OrderInParent', blank=True, null=True)
    timearchived = models.DateTimeField(db_column='TimeArchived', blank=True, null=True)
    timeexpiring = models.DateTimeField(db_column='TimeExpiring', blank=True, null=True)
    archiveflags = models.IntegerField(db_column='ArchiveFlags', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ArchiveEntry_T'


class ArchiveindicesT(models.Model):
    indexid = models.CharField(db_column='IndexID', max_length=36, blank=True, null=True)
    indextype = models.IntegerField(db_column='IndexType')
    value = models.CharField(db_column='Value', max_length=100, blank=True, null=True)
    archiveentry = models.CharField(db_column='ArchiveEntry', max_length=36)
    parent = models.CharField(db_column='Parent', max_length=36, blank=True, null=True)
    timeexpiring = models.DateTimeField(db_column='TimeExpiring', blank=True, null=True)
    modified = models.DateTimeField(db_column='Modified', blank=True, null=True)
    acl = models.CharField(db_column='ACL', max_length=36, blank=True, null=True)
    syncflag = models.IntegerField(db_column='SyncFlag', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ArchiveIndices_T'


class ArchivedjobsT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)
    cardinality = models.IntegerField(db_column='Cardinality', blank=True, null=True)
    amountpaid = models.FloatField(db_column='AmountPaid', blank=True, null=True)
    jobname = models.CharField(db_column='JobName', max_length=250, blank=True, null=True)
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ArchivedJobs_T'


class BasystemlogT(models.Model):
    entrytime = models.DateTimeField(db_column='EntryTime')
    entrytype = models.IntegerField(db_column='EntryType', blank=True, null=True)
    jobid = models.CharField(db_column='JobID', max_length=36, blank=True, null=True)
    description = models.CharField(db_column='Description', max_length=150, blank=True, null=True)
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)
    servername = models.CharField(db_column='ServerName', max_length=50, blank=True, null=True)
    logdata1 = models.CharField(db_column='LogData1', max_length=150, blank=True, null=True)
    logdata2 = models.CharField(db_column='LogData2', max_length=150, blank=True, null=True)
    entryid = models.IntegerField(db_column='EntryID', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BaSystemLog_T'


class BudgettransactionsT(models.Model):
    transactiontime = models.DateTimeField(db_column='TransactionTime', primary_key=True)
    transactiontype = models.IntegerField(db_column='TransactionType')
    amount = models.FloatField(db_column='Amount', blank=True, null=True)
    # entity = models.CharField(db_column='Entity', max_length=36)
    entity = models.ForeignKey('ServiceconsumerT', db_column='Entity')
    # service = models.CharField(db_column='Service', max_length=36, blank=True, null=True)
    service = models.ForeignKey('ServiceT', db_column='Service', primary_key=True)
    # serviceusage = models.CharField(db_column='ServiceUsage', max_length=36, blank=True, null=True)
    serviceusage = StringUUIDField(db_column='ServiceUsage', blank=True, null=True)
    transactiondata = models.CharField(db_column='TransactionData', max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BudgetTransactions_T'
        unique_together = ('entity', 'transactiontime', 'service')


class Camipro(models.Model):
    sciper = models.CharField(db_column='Sciper', max_length=6, primary_key=True)
    cardid = models.CharField(db_column='CardId', max_length=16, unique=True)

    class Meta:
        managed = False
        db_table = 'Camipro'


class CamiproOld(models.Model):
    sciper = models.CharField(db_column='Sciper', max_length=6, blank=True, null=True)
    cardid = models.CharField(db_column='CardId', max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Camipro_old'


class Centrefraisunite(models.Model):
    cf = models.CharField(db_column='CF', max_length=6, blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=32, blank=True, null=True)
    invoice = models.CharField(db_column='Invoice', max_length=1, blank=True, null=True)
    manager = models.CharField(db_column='Manager', max_length=6, blank=True, null=True)
    deputy = models.CharField(db_column='Deputy', max_length=6, blank=True, null=True)
    hierarchy = models.CharField(db_column='Hierarchy', max_length=128, blank=True, null=True)
    priceprofile = models.CharField(db_column='PriceProfile', max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CentreFraisUnite'


class ConfigobjectsT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ConfigObjects_T'


class ConsumergrouplinksT(models.Model):
    upperlink = models.CharField(db_column='UpperLink', max_length=36)
    lowerlink = models.CharField(db_column='LowerLink', max_length=36)

    class Meta:
        managed = False
        db_table = 'ConsumerGroupLinks_T'


class ConsumeridentitiesT(models.Model):
    # id = models.CharField(db_column='ID', max_length=36, primary_key=True)
    id = StringUUIDField(db_column='ID', primary_key=True)
    classdata = models.BinaryField(db_column='ClassData')
    # consumerid = models.CharField(db_column='ConsumerID', max_length=36)
    consumerid = StringUUIDField(db_column='ConsumerID', primary_key=True)
    identitycategory = models.IntegerField(db_column='IdentityCategory')
    identitytype = models.CharField(db_column='IdentityType', max_length=50, blank=True, null=True)
    value = models.CharField(db_column='Value', max_length=255, blank=True, null=True)
    defaultidentity = models.IntegerField(db_column='DefaultIdentity', blank=True, null=True)
    visibility = models.IntegerField(db_column='Visibility', blank=True, null=True)
    dispositionchecked = models.IntegerField(db_column='DispositionChecked', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ConsumerIdentities_T'

    def __str__(self):
        return self.value


class Copernic(models.Model):
    sciper = models.CharField(db_column='Sciper', max_length=50)
    unit = models.CharField(db_column='Unit', max_length=50)
    cf = models.CharField(db_column='CF', max_length=50)
    changetype = models.CharField(db_column='ChangeType', max_length=50, blank=True, null=True)
    priceprofile = models.CharField(db_column='PriceProfile', max_length=50)
    defaultcf = models.SmallIntegerField(db_column='DefaultCF')

    class Meta:
        managed = False
        db_table = 'Copernic'


class Copernic2(models.Model):
    sciper = models.CharField(db_column='Sciper', max_length=6, blank=True, null=True)
    unit = models.CharField(db_column='Unit', max_length=32, blank=True, null=True)
    cf = models.CharField(db_column='CF', max_length=6, blank=True, null=True)
    defaultcf = models.CharField(db_column='DefaultCF', max_length=1, blank=True, null=True)
    updated = models.IntegerField(db_column='Updated')

    class Meta:
        managed = False
        db_table = 'Copernic2'


class CostsavingsT(models.Model):
    usagebegin = models.DateTimeField(db_column='UsageBegin')
    usageend = models.DateTimeField(db_column='UsageEnd')
    serviceproviderinput = models.CharField(db_column='ServiceProviderInput', max_length=36)
    serviceprovider = models.CharField(db_column='ServiceProvider', max_length=36)
    serviceconsumer = models.CharField(db_column='ServiceConsumer', max_length=36)
    servconsgroup = models.CharField(db_column='ServConsGroup', max_length=36)
    servconsproject = models.CharField(db_column='ServConsProject', max_length=36)
    jobname = models.CharField(db_column='JobName', max_length=250, blank=True, null=True)
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True)
    formatcode = models.IntegerField(db_column='FormatCode')
    pages = models.IntegerField(db_column='Pages')
    pagescolor = models.IntegerField(db_column='PagesColor')
    pagesduplex = models.IntegerField(db_column='PagesDuplex')
    costs = models.FloatField(db_column='Costs', blank=True, null=True)
    costssaved = models.FloatField(db_column='CostsSaved', blank=True, null=True)
    costssavedpot = models.FloatField(db_column='CostsSavedPot', blank=True, null=True)
    type = models.IntegerField(db_column='Type')
    typepot = models.IntegerField(db_column='TypePot')

    class Meta:
        managed = False
        db_table = 'CostSavings_T'


class CountercheckT(models.Model):
    serviceprovider = models.CharField(db_column='ServiceProvider', max_length=36)
    timestamp = models.DateTimeField(db_column='Timestamp')
    servicecode = models.IntegerField(db_column='ServiceCode', blank=True, null=True)
    counterorigin = models.IntegerField(db_column='CounterOrigin', blank=True, null=True)
    value = models.IntegerField(db_column='Value', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CounterCheck_T'


class EventsT(models.Model):
    time = models.DateTimeField(db_column='Time')
    device = models.CharField(db_column='Device', max_length=36)
    serialnumber = models.CharField(db_column='SerialNumber', max_length=50, blank=True, null=True)
    devicetype = models.IntegerField(db_column='DeviceType', blank=True, null=True)
    eventtype = models.IntegerField(db_column='EventType', blank=True, null=True)
    status = models.IntegerField(db_column='Status', blank=True, null=True)
    statusex = models.CharField(db_column='StatusEx', max_length=64, blank=True, null=True)
    statuschange = models.CharField(db_column='StatusChange', max_length=64, blank=True, null=True)
    description = models.CharField(db_column='Description', max_length=150, blank=True, null=True)
    assocentity = models.CharField(db_column='AssocEntity', max_length=50, blank=True, null=True)
    totalcounter = models.IntegerField(db_column='TotalCounter', blank=True, null=True)
    manufacturerinfo = models.CharField(db_column='ManufacturerInfo', max_length=150, blank=True, null=True)
    systemservername = models.CharField(db_column='SystemServerName', max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Events_T'


class GroupmembershipT(models.Model):
    user = models.ForeignKey('ServiceconsumerT', db_column='UserID', primary_key=True,
                             related_name='groupmembershipt_user_set')
    group = models.ForeignKey('ServiceconsumerT', db_column='GroupID', related_name='groupmembershipt_group_set',
                              blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GroupMembership_T'
        unique_together = ('user', 'group')


class MomsystemtasksT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)
    type = models.CharField(db_column='Type', max_length=50, blank=True, null=True)
    lastexecution = models.DateTimeField(db_column='LastExecution', blank=True, null=True)
    nextexecution = models.DateTimeField(db_column='NextExecution', blank=True, null=True)
    lastexecutionresult = models.IntegerField(db_column='LastExecutionResult', blank=True, null=True)
    lasterror = models.CharField(db_column='LastError', max_length=50, blank=True, null=True)
    machinename = models.CharField(db_column='MachineName', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MomSystemTasks_T'


class ObjecthistoryT(models.Model):
    version = models.BigIntegerField(db_column='Version')
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)
    parentid = models.CharField(db_column='ParentID', max_length=36, blank=True, null=True)
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)
    objecttype = models.CharField(db_column='ObjectType', max_length=50, blank=True, null=True)
    objectname = models.CharField(db_column='ObjectName', max_length=50, blank=True, null=True)
    modified = models.DateTimeField(db_column='Modified', blank=True, null=True)
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=50, blank=True, null=True)
    description = models.CharField(db_column='Description', max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ObjectHistory_T'


class OrderitemsT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)
    orderid = models.CharField(db_column='OrderID', max_length=36)
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)
    amountpaid = models.FloatField(db_column='AmountPaid', blank=True, null=True)
    copycount = models.IntegerField(db_column='CopyCount', blank=True, null=True)
    vat = models.FloatField(db_column='VAT', blank=True, null=True)
    pricedetailtext = models.CharField(db_column='PriceDetailText', max_length=2048, blank=True, null=True)
    producttype = models.IntegerField(db_column='ProductType', blank=True, null=True)
    queuename = models.CharField(db_column='QueueName', max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'OrderItems_T'


class OrderT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)
    time = models.DateTimeField(db_column='Time')
    userid = models.CharField(db_column='UserID', max_length=36)
    number = models.CharField(db_column='Number', max_length=50, blank=True, null=True)
    status = models.IntegerField(db_column='Status', blank=True, null=True)
    visibility = models.IntegerField(db_column='Visibility', blank=True, null=True)
    cardtransaction = models.CharField(db_column='CardTransaction', max_length=36, blank=True, null=True)
    paymentmethod = models.CharField(db_column='PaymentMethod', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Order_T'


class PeersT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Peers_T'


class PrintjobhistoryT(models.Model):
    jobid = models.CharField(db_column='JobID', max_length=36)
    time = models.DateTimeField(db_column='Time')
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True)
    fieldname = models.CharField(db_column='FieldName', max_length=50, blank=True, null=True)
    oldvalue = models.CharField(db_column='OldValue', max_length=250, blank=True, null=True)
    newvalue = models.CharField(db_column='NewValue', max_length=250, blank=True, null=True)
    description = models.CharField(db_column='Description', max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PrintJobHistory_T'


class PrinterclusterT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)
    momsyncflag = models.NullBooleanField(db_column='MomSyncFlag')
    clusterrole = models.IntegerField(db_column='ClusterRole', blank=True, null=True)
    productfamily = models.IntegerField(db_column='ProductFamily', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PrinterCluster_T'


class Reportdata(models.Model):
    transactglobalid = models.CharField(db_column='TransactGlobalID', max_length=36, blank=True, null=True)
    jobdate = models.DateTimeField(db_column='JobDate', blank=True, null=True)
    resourcetype = models.CharField(db_column='ResourceType', max_length=2)
    pgecnt = models.IntegerField(db_column='PgeCnt', blank=True, null=True)
    cost = models.FloatField(db_column='Cost', blank=True, null=True)
    costcoloured = models.FloatField(db_column='CostColoured', blank=True, null=True)
    costbw = models.FloatField(db_column='CostBW', blank=True, null=True)
    pagescoloured = models.IntegerField(db_column='PagesColoured', blank=True, null=True)
    pagesbw = models.IntegerField(db_column='PagesBW', blank=True, null=True)
    completepgecnt = models.IntegerField(db_column='CompletePgeCnt', blank=True, null=True)
    pagesa4 = models.IntegerField(db_column='PagesA4', blank=True, null=True)
    pagesa3 = models.IntegerField(db_column='PagesA3', blank=True, null=True)
    pagesother = models.IntegerField(db_column='PagesOther', blank=True, null=True)
    cc = models.CharField(db_column='CC', max_length=50, blank=True, null=True)
    ccdesc = models.CharField(db_column='CCDesc', max_length=50, blank=True, null=True)
    ccid = models.CharField(db_column='CCID', max_length=36, blank=True, null=True)
    invoiceflag = models.CharField(db_column='InvoiceFlag', max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ReportData'


class ServiceconsumerT(models.Model):
    id = StringUUIDField(db_column='ID', primary_key=True)
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)
    login = models.CharField(db_column='Login', max_length=50, blank=True, null=True)
    defaultgroupid = StringUUIDField(db_column='DefaultGroupID', blank=True, null=True)
    usertypeex = models.IntegerField(db_column='UserTypeEx', blank=True, null=True)
    payconid = models.ForeignKey('Camipro', to_field='cardid', db_column='PayConID')
    usertype = models.CharField(db_column='UserType', max_length=20, blank=True, null=True)
    addressone = models.CharField(db_column='AddressOne', max_length=50, blank=True, null=True)
    addresstwo = models.CharField(db_column='AddressTwo', max_length=100, blank=True, null=True)
    zip = models.CharField(db_column='Zip', max_length=20, blank=True, null=True)
    city = models.CharField(db_column='City', max_length=50, blank=True, null=True)
    phone = models.CharField(db_column='Phone', max_length=50, blank=True, null=True)
    fax = models.CharField(db_column='Fax', max_length=50, blank=True, null=True)
    memo = models.CharField(db_column='Memo', max_length=250, blank=True, null=True)
    defaultcostcenter = StringUUIDField(db_column='DefaultCostCenter', blank=True, null=True)
    hasbiodata = models.IntegerField(db_column='HasBioData', blank=True, null=True)
    visibility = models.IntegerField(db_column='Visibility', blank=True, null=True)
    emergencyaccountflag = models.NullBooleanField(db_column='EmergencyAccountFlag')
    cslogininfo = models.CharField(db_column='CsLoginInfo', max_length=50, blank=True, null=True)
    sapname = models.CharField(db_column='SAPName', max_length=50, blank=True, null=True)
    pincodehash = models.CharField(db_column='PinCodeHash', max_length=80, blank=True, null=True)
    momsyncflag = models.NullBooleanField(db_column='MomSyncFlag')
    linkedconsumerid = StringUUIDField(db_column='LinkedConsumerID', blank=True, null=True)
    modified = models.DateTimeField(db_column='Modified', blank=True, null=True)
    customprop_igstatus = models.CharField(db_column='CustomProp_IGStatus', max_length=5, blank=True, null=True)
    customprop_iglogin = models.CharField(db_column='CustomProp_IGLOGIN', max_length=50, blank=True, null=True)
    state = models.CharField(db_column='State', max_length=10, blank=True, null=True)
    hierarchyposition = StringUUIDField(db_column='HierarchyPosition', blank=True, null=True)
    forcedrilldown = models.IntegerField(db_column='ForceDrillDown', blank=True, null=True)
    emailaddress = models.CharField(db_column='EmailAddress', max_length=50, blank=True, null=True)
    objectcontainerversion = models.IntegerField(db_column='OBJECTCONTAINERVERSION', blank=True, null=True)
    entitylinked = models.ManyToManyField('ServiceconsumerT', through='GroupmembershipT',
                                          through_fields=('group', 'user'))

    class Meta:
        managed = False
        db_table = 'ServiceConsumer_T'

    def __str__(self):
        return '{} : {}/{}'.format(self.id, self.name, self.login)


class ServiceproviderT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)
    payconserialno = models.CharField(db_column='PayConSerialNo', max_length=50, blank=True, null=True)
    displayindex = models.IntegerField(db_column='DisplayIndex', blank=True, null=True)
    printername = models.CharField(db_column='PrinterName', max_length=150, blank=True, null=True)
    routinggroup = models.CharField(db_column='RoutingGroup', max_length=50, blank=True, null=True)
    servername = models.CharField(db_column='ServerName', max_length=50, blank=True, null=True)
    payconipaddress = models.CharField(db_column='PayConIpAddress', max_length=50, blank=True, null=True)
    providertype = models.IntegerField(db_column='ProviderType', blank=True, null=True)
    pricingprofile = models.CharField(db_column='PricingProfile', max_length=36, blank=True, null=True)
    hideprinterfromwqm = models.IntegerField(db_column='HidePrinterFromWqm', blank=True, null=True)
    visibility = models.IntegerField(db_column='Visibility', blank=True, null=True)
    mgmtdata_customernumber = models.CharField(db_column='MgmtData_CustomerNumber', max_length=50,
                                               blank=True, null=True)
    mgmtdata_monthlyvolume = models.CharField(db_column='MgmtData_MonthlyVolume', max_length=50, blank=True, null=True)
    mgmtdata_contractstart = models.CharField(db_column='MgmtData_ContractStart', max_length=50, blank=True, null=True)
    mgmtdata_contractend = models.CharField(db_column='MgmtData_ContractEnd', max_length=50, blank=True, null=True)
    mgmtdata_serial = models.CharField(db_column='MgmtData_Serial', max_length=50, blank=True, null=True)
    mgmtdata_location = models.CharField(db_column='MgmtData_Location', max_length=50, blank=True, null=True)
    mgmtdata_assetnumber = models.CharField(db_column='MgmtData_AssetNumber', max_length=50, blank=True, null=True)
    mgmtdata_hostname = models.CharField(db_column='MgmtData_Hostname', max_length=50, blank=True, null=True)
    mgmtdata_macaddress = models.CharField(db_column='MgmtData_MacAddress', max_length=50, blank=True, null=True)
    mgmtdata_modelname = models.CharField(db_column='MgmtData_ModelName', max_length=50, blank=True, null=True)
    momsyncflag = models.NullBooleanField(db_column='MomSyncFlag')
    modified = models.DateTimeField(db_column='Modified', blank=True, null=True)
    wizardname = models.CharField(db_column='WizardName', max_length=50, blank=True, null=True)
    mgmtdata_manufacturer = models.CharField(db_column='MgmtData_Manufacturer', max_length=50, blank=True, null=True)
    mgmtdata_productfamily = models.CharField(db_column='MgmtData_ProductFamily', max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ServiceProvider_T'


class ServiceusagecontainerinfoT(models.Model):
    jobid = models.CharField(db_column='JobID', max_length=36)
    jobkey = models.CharField(db_column='JobKey', max_length=50, blank=True, null=True)
    jobvalue = models.CharField(db_column='JobValue', max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ServiceUsageContainerInfo_T'


class ServiceusageT(models.Model):
    id = StringUUIDField(db_column='ID', primary_key=True)
    serviceprovider = models.CharField(db_column='ServiceProvider', max_length=36)
    service = models.ForeignKey('ServiceT', db_column='Service')
    serviceconsumer = models.ForeignKey(ServiceconsumerT, db_column='ServiceConsumer')
    servconsgroup = models.ForeignKey(ServiceconsumerT, db_column='ServConsGroup',
                                      related_name='serviceusage_servconsgroup_set')
    servconsproject = models.ForeignKey(ServiceconsumerT, db_column='ServConsProject',
                                        related_name='serviceusage_servconsproject_set')
    cardnumber = models.IntegerField(db_column='CardNumber', blank=True, null=True)
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)
    usagebegin = models.DateTimeField(db_column='UsageBegin', blank=True, null=True)
    usageend = models.DateTimeField(db_column='UsageEnd', blank=True, null=True)
    cardinality = models.IntegerField(db_column='Cardinality', blank=True, null=True)
    amountpaid = models.FloatField(db_column='AmountPaid', blank=True, null=True)
    parentservice = models.CharField(db_column='ParentService', max_length=36, blank=True, null=True)
    jobname = models.CharField(db_column='JobName', max_length=250, blank=True, null=True)
    username = models.CharField(db_column='UserName', max_length=50, blank=True, null=True)
    streamversion = models.CharField(db_column='StreamVersion', max_length=30, blank=True, null=True)
    jobticketfield = models.CharField(db_column='JobTicketField', max_length=60, blank=True, null=True)
    jobticketfieldtwo = models.CharField(db_column='JobTicketFieldTwo', max_length=60, blank=True, null=True)
    jobticketfieldthree = models.CharField(db_column='JobTicketFieldThree', max_length=60, blank=True, null=True)
    copycount = models.IntegerField(db_column='CopyCount', blank=True, null=True)
    nonchargeable = models.IntegerField(db_column='NonChargeable', blank=True, null=True)
    nonchargereason = models.CharField(db_column='NonChargeReason', max_length=255, blank=True, null=True)
    momsyncflag = models.NullBooleanField(db_column='MomSyncFlag')
    altprice0 = models.FloatField(db_column='AltPrice0', blank=True, null=True)
    altprice1 = models.FloatField(db_column='AltPrice1', blank=True, null=True)
    altprice2 = models.FloatField(db_column='AltPrice2', blank=True, null=True)
    costsavings = models.FloatField(db_column='CostSavings', blank=True, null=True)
    cpcajobid = models.CharField(db_column='CpcaJobID', max_length=30, blank=True, null=True)
    costcenterpath = models.CharField(db_column='CostCenterPath', max_length=512, blank=True, null=True)
    jobsettings_cloneof = models.CharField(db_column='JobSettings_CloneOf', max_length=38, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ServiceUsage_T'


class ServiceT(models.Model):
    id = StringUUIDField(db_column='ID', primary_key=True)
    classdata = models.BinaryField(db_column='ClassData', blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)
    serviceprovider = models.CharField(db_column='ServiceProvider', max_length=36)
    servicecode = models.IntegerField(db_column='ServiceCode', blank=True, null=True)
    providerindex = models.IntegerField(db_column='ProviderIndex', blank=True, null=True)
    visibility = models.IntegerField(db_column='Visibility', blank=True, null=True)
    momsyncflag = models.NullBooleanField(db_column='MomSyncFlag')
    modified = models.DateTimeField(db_column='Modified', blank=True, null=True)
    acl = models.CharField(db_column='ACL', max_length=36, blank=True, null=True)
    jttag = models.CharField(db_column='JtTag', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Service_T'

    def get_service_name(self):
        code_to_name = {
            '0': '',
            '-1': 'General',
            '65537': 'Copy A4',
            '65538': 'Copy A3',
            '65539': 'Copy B4',
            '65540': 'Copy B3',
            '131073': 'Copy color A4',
            '131074': 'Copy color A3',
            '131075': 'Copy color B4',
            '131076': 'Copy color B3',
            '196609': 'Print A4',
            '196610': 'Print A3',
            '196611': 'Print B4',
            '196612': 'Print B3',
            '262145': 'Print color A4',
            '262146': 'Print color A3',
            '262147': 'Print color B4',
            '262148': 'Print color B3',
            '52429': 'Finishing option cutter',
            '524290': 'Finishing option sorter',
            '524291': 'Finishing option hole punching',
            '524292': 'Finishing option stapling',
            '524293': 'Finishing option Binding'
        }

        try:
            to_return = code_to_name[str(self.servicecode)]
        except KeyError:
            to_return = ''
        return to_return


class SinglerowstatT(models.Model):
    entrytime = models.DateTimeField(db_column='EntryTime')
    username = models.CharField(db_column='UserName', max_length=15, blank=True, null=True)
    jobname = models.CharField(db_column='JobName', max_length=250, blank=True, null=True)
    printername = models.CharField(db_column='PrinterName', max_length=20, blank=True, null=True)
    servername = models.CharField(db_column='ServerName', max_length=20, blank=True, null=True)
    formatcode = models.IntegerField(db_column='FormatCode')
    totalpages = models.IntegerField(db_column='TotalPages')
    duplexpages = models.IntegerField(db_column='DuplexPages')
    colorpages = models.IntegerField(db_column='ColorPages')
    inputtray = models.SmallIntegerField(db_column='InputTray')

    class Meta:
        managed = False
        db_table = 'SingleRowStat_T'


class VendingtransactionsT(models.Model):
    id = models.CharField(db_column='ID', max_length=36, primary_key=True)
    classdata = models.BinaryField(db_column='ClassData')
    consumerid = models.CharField(db_column='ConsumerID', max_length=36)

    class Meta:
        managed = False
        db_table = 'VendingTransactions_T'
