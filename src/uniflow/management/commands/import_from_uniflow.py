import re

from django.db.models import Q
from django.core.management.base import BaseCommand

from uniflow.models import ServiceusageT, ServiceconsumerT, GroupmembershipT, Camipro
from bill2myprint.models import Student, Semester, Transaction, Section


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

    def handle(self, *args, **options):
        date_last_imported = Transaction.objects.order_by('-transaction_date')[0].transaction_date
        students_group_id = ServiceconsumerT.objects.get(name='Etudiant').id
        students_cost_center_id = ServiceconsumerT.objects.get(name='ETU').id
        students = ServiceconsumerT.objects.filter(defaultgroupid=students_group_id,
                                                   defaultcostcenter=students_cost_center_id).exclude(payconid='')
        i = 0
        for student_uniflow in students:
            i += 1
            print('Student : {}, {}'.format(i, student_uniflow))
            try:
                student_sciper = student_uniflow.payconid.sciper
            except Camipro.DoesNotExist:
                continue
            student = Student.objects.get_or_create(sciper=student_sciper)[0]
            to_save = []
            if options['first']:
                student_transactions = student_uniflow.serviceusaget_set.all().order_by('usagebegin')
            else:
                student_transactions = student_uniflow.serviceusaget_set.filter(usagebegin__gt=date_last_imported).order_by('usagebegin')
            try:
                uniflow_section = student_uniflow.groupmembershipt_user_set.get(group__name__iendswith='S_StudU').group.name
            except GroupmembershipT.DoesNotExist:
                continue
            section_acronym = re.search('(.*)S_StudU', uniflow_section).group(1)
            try:
                section = Section.objects.get(acronym=section_acronym)
            except Section.DoesNotExist:
                continue
            for st in student_transactions:
                if st.amountpaid == 0:
                    continue
                elif st.amountpaid < 0:
                    transaction_type = 'REFUND'
                else:
                    transaction_type = 'PRINT_JOB'
                semester = Semester.objects.filter(end_date__gte=st.usagebegin)[0]
                to_save.append(Transaction(
                    transaction_type=transaction_type,
                    transaction_date=st.usagebegin,
                    semester=semester,
                    amount=-st.amountpaid,
                    section=section,
                    student=student,
                    cardinality=st.cardinality,
                    job_type=st.service.get_service_name())
                )

            uniflow_budget_transactions = student_uniflow.budgettransactionst_set.filter(Q(transactiondata__icontains='Allocation') |
                                                                                         Q(transactiondata__icontains='Rallonge') |
                                                                                         Q(transactiondata__icontains='Camipro-Web-Load'))
            for bt in uniflow_budget_transactions:
                semester = Semester.objects.filter(end_date__gte=bt.transactiontime)[0]
                if 'allocation' in bt.transactiondata.lower():
                    to_save.append(Transaction(
                        transaction_type='MYPRINT_ALLOWANCE',
                        transaction_date=bt.transactiontime,
                        semester=semester,
                        amount=-bt.amount,
                        section=section,
                        student=student,
                        cardinality=1,
                        job_type='')
                    )
                elif 'rallonge' in bt.transactiondata.lower():
                    to_save.append(Transaction(
                        transaction_type='FACULTY_ALLOWANCE',
                        transaction_date=bt.transactiontime,
                        semester=semester,
                        amount=-bt.amount,
                        section=section,
                        student=student,
                        cardinality=1,
                        job_type='')
                    )
                elif 'camipro-web-load' in bt.transactiondata.lower():
                    to_save.append(Transaction(
                        transaction_type='ACCOUNT_CHARGING',
                        transaction_date=bt.transactiontime,
                        semester=semester,
                        amount=-bt.amount,
                        section=section,
                        student=student,
                        cardinality=1,
                        job_type='')
                    )
                else:
                    raise ValueError('Unknown transaction type in uniflow')

            Transaction.objects.bulk_create(to_save)
