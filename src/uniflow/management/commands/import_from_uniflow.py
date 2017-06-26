import re
from datetime import timedelta

from django.db.models import Q
from django.core.management.base import BaseCommand

from uniflow.models import ServiceusageT, ServiceconsumerT, GroupmembershipT, Camipro, BudgettransactionsT
from bill2myprint.models import Student, Semester, Transaction, Section, SemesterSummary, UpdateStatus
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
                pattern = re.compile("^\d{6}$")
                if pattern.match(username):
                    student_sciper = username
                    username = VPersonDeltaHistory.get_username_at_time(student_sciper, transaction_time)
                    name = VPersonDeltaHistory.get_name_at_time(student_sciper, transaction_time)
                else:
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

    def handle_initial_allowance(self, student, section, semester):
        first_uniflow_semester = Semester.objects.get(name='Automne 2016-2017')
        if semester.end_date < first_uniflow_semester.end_date:
            semester = first_uniflow_semester
        dt = timedelta(days=1)
        d = semester.end_date_official - dt
        if not student.has_uniflow_initial_allowance:
            Transaction.objects.create(transaction_type='MYPRINT_ALLOWANCE',
                                       transaction_date=d,
                                       semester=semester,
                                       amount=24.0,
                                       section=section,
                                       student=student,
                                       cardinality=1,
                                       job_type=''
                                       )
            self.update_semester_summary(student=student,
                                         section=section,
                                         semester=semester,
                                         transaction_type='MYPRINT_ALLOWANCE',
                                         amount=-24
                                         )
            student.has_uniflow_initial_allowance = True
            student.save()

    def handle_myprint_allowance(self, first):
        date_last_imported = Transaction.objects.order_by('-transaction_date')[0].transaction_date
        # If it is the first time this script is run, then take all transactions else take only new ones
        if first:
            uniflow_budget_transactions = BudgettransactionsT.objects.filter(Q(transactiondata__icontains='Alloc'))
        else:
            uniflow_budget_transactions = BudgettransactionsT.objects.filter(Q(transactiondata__icontains='Alloc') &
                                                                             Q(transactiontime__gt=date_last_imported))
        uniflow_budget_transactions = uniflow_budget_transactions.order_by('entity', 'transactiontime')

        current_serviceconsumer_id = ''
        to_save = []
        print('MyPrint allowance')
        # This loop handles BudgetTransactions, it uses the same principles as the previous one.
        for bt in uniflow_budget_transactions:
            if not current_serviceconsumer_id or current_serviceconsumer_id != bt.entity.id:
                current_serviceconsumer_id = ''
                student = self.get_student(bt.entity, bt.transactiontime)
                if student is None:
                    continue
                section = self.get_section(bt.entity, student, bt.transactiontime)
                if not section:
                    continue
                current_serviceconsumer_id = bt.entity.id
            if bt.amount == 0:
                    continue
            semester = None
            if 'alloc' in bt.transactiondata.lower():
                transaction_type = 'MYPRINT_ALLOWANCE'
                semester = Semester.objects.filter(end_date_official__gte=bt.transactiontime).order_by('end_date')[0]
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
            semester = Semester.objects.filter(end_date_official__lt=bt.transactiontime).order_by('-end_date')[0]
            self.handle_initial_allowance(student=student, section=section, semester=semester)
        Transaction.objects.bulk_create(to_save)

    def handle_faculty_allowance(self, first):
        date_last_imported = Transaction.objects.order_by('-transaction_date')[0].transaction_date
        # If it is the first time this script is run, then take all transactions else take only new ones
        if first:
            uniflow_budget_transactions = BudgettransactionsT.objects.filter(Q(transactiondata__icontains='Rallonge'))
        else:
            uniflow_budget_transactions = BudgettransactionsT.objects.filter(Q(transactiondata__icontains='Rallonge') &
                                                                             Q(transactiontime__gt=date_last_imported))
        uniflow_budget_transactions = uniflow_budget_transactions.order_by('entity', 'transactiontime')

        current_serviceconsumer_id = ''
        to_save = []
        # This loop handles BudgetTransactions, it uses the same principles as the previous one.
        print('Faculty allowance')
        for bt in uniflow_budget_transactions:
            if not current_serviceconsumer_id or current_serviceconsumer_id != bt.entity.id:
                current_serviceconsumer_id = ''
                student = self.get_student(bt.entity, bt.transactiontime)
                if student is None:
                    continue
                section = self.get_section(bt.entity, student, bt.transactiontime)
                if not section:
                    continue
                current_serviceconsumer_id = bt.entity.id
            if bt.amount == 0:
                    continue
            semester = None
            if 'rallonge' in bt.transactiondata.lower():
                transaction_type = 'FACULTY_ALLOWANCE'
                semester = Semester.objects.filter(end_date_official__gte=bt.transactiontime).order_by('end_date')[0]
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
            self.handle_initial_allowance(student=student, section=section, semester=semester)
        Transaction.objects.bulk_create(to_save)

    def handle_account_charging(self, first):
        date_last_imported = Transaction.objects.order_by('-transaction_date')[0].transaction_date
        # If it is the first time this script is run, then take all transactions else take only new ones
        if first:
            uniflow_budget_transactions = BudgettransactionsT.objects.filter(Q(transactiondata__icontains='Camipro-Web-Load'))
        else:
            uniflow_budget_transactions = BudgettransactionsT.objects.filter(Q(transactiondata__icontains='Camipro-Web-Load') &
                                                                             Q(transactiontime__gt=date_last_imported))
        uniflow_budget_transactions = uniflow_budget_transactions.order_by('entity', 'transactiontime')

        current_serviceconsumer_id = ''
        to_save = []
        print('Account Charging')
        # This loop handles BudgetTransactions, it uses the same principles as the previous one.
        for bt in uniflow_budget_transactions:
            if not current_serviceconsumer_id or current_serviceconsumer_id != bt.entity.id:
                current_serviceconsumer_id = ''
                student = self.get_student(bt.entity, bt.transactiontime)
                if student is None:
                    continue
                section = self.get_section(bt.entity, student, bt.transactiontime)
                if not section:
                    continue
                current_serviceconsumer_id = bt.entity.id
            if bt.amount == 0:
                    continue
            semester = None
            if 'camipro-web-load' in bt.transactiondata.lower():
                transaction_type = 'ACCOUNT_CHARGING'
                semester = Semester.objects.filter(end_date__gte=bt.transactiontime).order_by('end_date')[0]
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
            self.handle_initial_allowance(student=student, section=section, semester=semester)
        Transaction.objects.bulk_create(to_save)

    def handle(self, *args, **options):
        date_last_imported = Transaction.objects.order_by('-transaction_date')[0].transaction_date
        students_cost_center_id = ServiceconsumerT.objects.get(name='ETU').id
        # If it is the first time this script is run, then take all transactions else take only new ones
        if options['first']:
            self.handle_myprint_allowance(True)
            self.handle_faculty_allowance(True)
            self.handle_account_charging(True)
            service_usages = ServiceusageT.objects.filter(costcenterpath__icontains=students_cost_center_id)
        else:
            self.handle_myprint_allowance(False)
            self.handle_faculty_allowance(False)
            self.handle_account_charging(False)
            service_usages = ServiceusageT.objects.filter(usagebegin__gt=date_last_imported,
                                                          costcenterpath__icontains=students_cost_center_id)
        service_usages = service_usages.order_by('serviceconsumer', 'usagebegin')
        batch = 5000

        total = service_usages.count()
        current_serviceconsumer_id = ''
        next_batch_start = 0
        batch_end = 0
        # This loop handles ServiceUsage objects (print jobs)
        while batch_end < total:
            batch_end = min(total, batch_end + batch)
            to_save = []
            for su in service_usages[next_batch_start:batch_end]:
                # This is only implemented to limit the number of database query we run
                if not current_serviceconsumer_id or current_serviceconsumer_id != su.serviceconsumer.id:
                    current_serviceconsumer_id = ''
                    student = self.get_student(su.serviceconsumer, su.usagebegin)
                    if student is None:
                        continue
                    section = self.get_section(su.serviceconsumer, student, su.usagebegin)
                    if not section:
                        continue
                    current_serviceconsumer_id = su.serviceconsumer.id
                    semester = Semester.objects.filter(end_date__gte=su.usagebegin).order_by('end_date')[0]
                    self.handle_initial_allowance(student=student, section=section, semester=semester)
                if su.amountpaid == 0:
                        continue
                elif su.amountpaid < 0:
                    transaction_type = 'REFUND'
                else:
                    transaction_type = 'PRINT_JOB'
                semester = Semester.objects.filter(end_date__gte=su.usagebegin).order_by('end_date')[0]
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

        date_last_transaction = Transaction.objects.order_by('-transaction_date')[0].transaction_date
        UpdateStatus.objects.create(status='SUCCESS', message='', update_date=date_last_transaction)
