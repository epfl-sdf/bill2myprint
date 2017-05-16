import re

from django.db.models import Q
from django.core.management.base import BaseCommand

from uniflow.models import ServiceusageT, ServiceconsumerT, GroupmembershipT, Camipro, BudgettransactionsT
from bill2myprint.models import Student, Semester, Transaction, Section, SemesterSummary


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

    def get_section_from_uniflow(self, student_uniflow):
        try:
            uniflow_section = student_uniflow.groupmembershipt_user_set.get(group__name__iendswith='S_StudU').group.name
        except (GroupmembershipT.DoesNotExist, GroupmembershipT.MultipleObjectsReturned):
            return None
        if uniflow_section:
            section_acronym = re.search('(.*)S_StudU', uniflow_section).group(1)
            try:
                section = Section.objects.get(acronym=section_acronym)
            except Section.DoesNotExist:
                return None
        return section

    def get_student_from_uniflow(self, student_uniflow):
        username = student_uniflow.login
        name = student_uniflow.name
        # Try to identify student with link between camipro card and sciper
        # If this link does not exist for this student identify him with his gaspar's username
        has_camipro = False
        try:
            student_sciper = student_uniflow.payconid.sciper
            has_camipro = True
        except Camipro.DoesNotExist:
            pass

        if has_camipro:
            student = Student.objects.filter(sciper=student_sciper)
            if student.count() == 0:
                student = Student.objects.create(sciper=student_sciper, username=username, name=name)
            else:
                assert student.count() == 1
                student = student[0]
                if student.name != name and name:
                    student.name=name
                    student.save()
                elif student.username != username and username:
                    student.username=username
                    student.save()
        else:
            try:
                student = Student.objects.get_or_create(username=username)[0]
            except Student.MultipleObjectsReturned:
                return None
            if student.name != name and name:
                student.name = name
                student.save()
        return student

    def update_semester_summary(self, student, section, semester, transaction_type, amount):
        summary = SemesterSummary.objects.filter(student=student, section=section, semester=semester)
        if summary.count() == 0:
            summary = SemesterSummary(student=student, section=section, semester=semester)
        else:
            assert summary.count() == 1
            summary = summary[0]
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
        service_usages = service_usages.order_by('serviceconsumer')
        batch = 10000
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
                    current_serviceconsumer_id = su.serviceconsumer.id
                    student = self.get_student_from_uniflow(su.serviceconsumer)
                    section = self.get_section_from_uniflow(su.serviceconsumer)
                if student is None or section is None:
                    continue
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
                    current_serviceconsumer_id = bt.entity.id
                    student = self.get_student_from_uniflow(bt.entity)
                    section = self.get_section_from_uniflow(bt.entity)
                if student is None or section is None:
                    continue
                if bt.amount == 0:
                        continue
                semester = Semester.objects.filter(end_date__gte=bt.transactiontime)[0]
                if 'alloc' in bt.transactiondata.lower():
                    transaction_type = 'MYPRINT_ALLOWANCE'
                elif 'rallonge' in bt.transactiondata.lower():
                    transaction_type = 'FACULTY_ALLOWANCE'
                elif 'camipro-web-load' in bt.transactiondata.lower():
                    transaction_type = 'ACCOUNT_CHARGING'
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
