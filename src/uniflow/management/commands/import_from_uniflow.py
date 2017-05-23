import re

from django.db.models import Q
from django.core.management.base import BaseCommand

from uniflow.models import ServiceusageT, ServiceconsumerT, GroupmembershipT, Camipro, BudgettransactionsT
from bill2myprint.models import Student, Semester, Transaction, Section, SemesterSummary
from staff.models import VPersonDeltaHistory


class Command(BaseCommand):
    help = 'Populates the database with sections and the faculties'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--first',
            action='store_true',
            dest='first',
            default=False,
        )

    def get_section(self, student_uniflow, student, transaction_time):
        section = None
        uniflow_section = None
        section_acronym = ''
        try:
            uniflow_section = student_uniflow.groupmembershipt_user_set.get(group__name__iendswith='S_StudU').group.name
            section_acronym = re.search('(.*)S_StudU', uniflow_section).group(1)
        except (GroupmembershipT.DoesNotExist, GroupmembershipT.MultipleObjectsReturned):
            section_acronym = VPersonDeltaHistory.get_section_acronym_at_time(student.sciper, transaction_time)
        try:
            section = Section.objects.get(acronym=section_acronym)
        except Section.DoesNotExist:
            return None
        return section

    def get_student(self, student_uniflow, transaction_time):
        username = student_uniflow.login
        name = student_uniflow.name
        # Try to identify student with link between camipro card and sciper
        # If this link does not exist for this student identify him with his gaspar's username
        try:
            student_sciper = student_uniflow.payconid.sciper
        except Camipro.DoesNotExist:
            student_sciper = VPersonDeltaHistory.get_sciper_at_time(username, transaction_time)
            if student_sciper is None:
                print('ATTENTION: {} {}'.format(username, transaction_time))
                return None
        student, created = Student.objects.get_or_create(sciper=student_sciper)
        if student.name != name and name:
            student.name = name
            student.save()
        if student.username != username and username:
            student.username = username
            student.save()
        return student

    def update_semester_summary(self, student, section, semester, transaction_type, amount):
        summary, created = SemesterSummary.objects.get_or_create(student=student, section=section, semester=semester)
        if transaction_type == 'REFUND' or transaction_type == 'PRINT_JOB':
            summary.total_spent -= amount
        elif transaction_type == 'MYPRINT_ALLOWANCE':
            summary.myprint_allowance -= amount
        elif transaction_type == 'FACULTY_ALLOWANCE':
            summary.faculty_allowance -= amount
        elif transaction_type == 'ACCOUNT_CHARGING':
            summary.total_charged -= amount
        else:
            raise ValueError('Unknown transaction type')
        summary.save()

    def handle(self, *args, **options):
        date_last_imported = Transaction.objects.order_by('-transaction_date')[0].transaction_date
        students_group_id = ServiceconsumerT.objects.get(name='Etudiant').id
        students_cost_center_id = ServiceconsumerT.objects.get(name='ETU').id
        # If it is the first time this script is run, then take all transactions else take only new ones
        if options['first']:
            service_usages = ServiceusageT.objects.filter(serviceconsumer__defaultgroupid=students_group_id,
                                                          serviceconsumer__defaultcostcenter=students_cost_center_id)
            uniflow_budget_transactions = BudgettransactionsT.objects.filter(Q(transactiondata__icontains='Alloc') |
                                                                             Q(transactiondata__icontains='Rallonge') |
                                                                             Q(transactiondata__icontains='Camipro-Web-Load'))
        else:
            service_usages = ServiceusageT.objects.filter(usagebegin__gt=date_last_imported,
                                                          serviceconsumer__defaultgroupid=students_group_id,
                                                          serviceconsumer__defaultcostcenter=students_cost_center_id)
            uniflow_budget_transactions = BudgettransactionsT.objects.filter(Q(transactiondata__icontains='Alloc') |
                                                                             Q(transactiondata__icontains='Rallonge') |
                                                                             Q(transactiondata__icontains='Camipro-Web-Load') &
                                                                             Q(transactiontime__gt=date_last_imported))
        service_usages = service_usages.order_by('serviceconsumer', 'usagebegin')
        uniflow_budget_transactions = uniflow_budget_transactions.order_by('entity', 'transactiontime')
        batch = 5000
        total = service_usages.count()
        next_batch_start = 0
        current_serviceconsumer_id = ''
        batch_end = 0
        # This loop handles ServiceUsage objects (print jobs)
        while batch_end < total:
            batch_end = min(total, batch_end + batch)
            print('Usages : ' + str(batch_end))
            to_save = []
            for su in service_usages[next_batch_start:batch_end]:
                try:
                    if su.serviceconsumer.defaultgroupid != students_group_id or su.serviceconsumer.defaultcostcenter != students_cost_center_id:
                        continue
                except ServiceconsumerT.DoesNotExist:
                    continue
                # This is only implemented to limit the number of database query we run
                if not current_serviceconsumer_id or current_serviceconsumer_id != su.serviceconsumer.id:
                    current_serviceconsumer_id = ''
                    student = self.get_student(su.serviceconsumer, su.usagebegin)
                    section = self.get_section(su.serviceconsumer, student, su.usagebegin)
                    if not section or student is None:
                        continue
                    current_serviceconsumer_id = su.serviceconsumer.id
                if su.amountpaid == 0:
                        continue
                elif su.amountpaid < 0:
                    transaction_type = 'REFUND'
                else:
                    transaction_type = 'PRINT_JOB'
                semester = Semester.objects.filter(end_date__gte=su.usagebegin)[0]
                to_save.append(Transaction(
                    transaction_type=transaction_type,
                    transaction_date=su.usagebegin,
                    semester=semester,
                    amount=-su.amountpaid,
                    section=section,
                    student=student,
                    cardinality=su.cardinality,
                    job_type=su.service.get_service_name())
                )
                self.update_semester_summary(student, section, semester, transaction_type, su.amountpaid)
            Transaction.objects.bulk_create(to_save)
            next_batch_start = batch_end

        total = uniflow_budget_transactions.count()
        current_serviceconsumer_id = ''
        next_batch_start = 0
        batch_end = 0
        # This loop handles BudgetTransactions, it uses the same principles as the previous one.
        while batch_end < total:
            batch_end = min(total, batch_end + batch)
            print('Budget : ' + str(batch_end))
            to_save = []
            for bt in uniflow_budget_transactions[next_batch_start:batch_end]:
                if bt.entity.defaultgroupid != students_group_id or bt.entity.defaultcostcenter != students_cost_center_id:
                    continue
                if not current_serviceconsumer_id or current_serviceconsumer_id != bt.entity.id:
                    current_serviceconsumer_id = ''
                    student = self.get_student(bt.entity, bt.transactiontime)
                    section = self.get_section(bt.entity, student, bt.transactiontime)
                    if not section or student is None:
                        continue
                    current_serviceconsumer_id = bt.entity.id
                if bt.amount == 0:
                        continue
                semester = None
                if 'alloc' in bt.transactiondata.lower():
                    transaction_type = 'MYPRINT_ALLOWANCE'
                    semester = Semester.objects.filter(end_date_official__gte=bt.transactiontime)[0]
                elif 'rallonge' in bt.transactiondata.lower():
                    transaction_type = 'FACULTY_ALLOWANCE'
                    semester = Semester.objects.filter(end_date_official__gte=bt.transactiontime)[0]
                elif 'camipro-web-load' in bt.transactiondata.lower():
                    transaction_type = 'ACCOUNT_CHARGING'
                    semester = Semester.objects.filter(end_date__gte=bt.transactiontime)[0]
                else:
                    raise ValueError('Unknown transaction type in uniflow')
                to_save.append(Transaction(
                    transaction_type=transaction_type,
                    transaction_date=bt.transactiontime,
                    semester=semester,
                    amount=-bt.amount,
                    section=section,
                    student=student,
                    cardinality=1,
                    job_type='')
                )
                self.update_semester_summary(student, section, semester, transaction_type, bt.amount)
            Transaction.objects.bulk_create(to_save)
            next_batch_start = batch_end
