import re

from django.db.models import Q, Count, Case, F, FloatField, When
from django.core.management.base import BaseCommand

from equitrac.models import TAllTransactions
from bill2myprint.models import Student, Semester, Transaction, Section, SemesterSummary


def xstr(s):
    if s is None:
        return ''
    return s


class Command(BaseCommand):
    help = 'Populates the database with sections and the faculties'

    def update_and_get_student(self, sciper, username):
        student = Student.objects.get(sciper=sciper)
        if student.username != username:
            student.username = username
            student.save()
        return student

    def handle(self, *args, **options):
        i = 0
        current_semester = None
        previous_semester = None
        to_save = []
        for semester in Semester.objects.all().order_by('end_date'):
            i += 1
            print('Semester: {}'.format(i))
            previous_semester = current_semester
            if not current_semester:
                current_semester = semester
                semester_transactions = TAllTransactions.objects.filter(trans_datetime__lte=current_semester.end_date_official)
            else:
                current_semester = semester
                semester_transactions = TAllTransactions.objects.filter(trans_datetime__lte=current_semester.end_date_official,
                                                                        trans_datetime__gt=previous_semester.end_date_official)

            semester_transactions = semester_transactions.filter(hierarchie2='EPFL ETU').filter(trans_origin='T_STUD_ALLOWANCE')
            semester_transactions = semester_transactions.exclude(Q(hierarchie3__icontains='audit') |
                                                                  Q(hierarchie3__icontains='EDOC'))
            semester_transactions = semester_transactions.values_list('person_sciper',
                                                                      'hierarchie3',
                                                                      'trans_datetime',
                                                                      'trans_amount',
                                                                      'trans_origin',
                                                                      'trans_description',
                                                                      'account_name')
            semester_transactions = semester_transactions.order_by('person_sciper', 'trans_datetime')

            current_sciper = ''
            current_section_acronym = ''
            last_transaction=None

            for st in semester_transactions:
                st_section_acronym = re.search('EPFL ETU (.*)-.*', st[1]).group(1)
                if not current_sciper:
                    current_sciper = st[0]
                    student = self.update_and_get_student(sciper=current_sciper, username=xstr(st[6]))
                if not current_section_acronym:
                    current_section_acronym = st_section_acronym
                    section = Section.objects.get(acronym=current_section_acronym)
                if current_sciper != st[0]:
                    current_sciper = st[0]
                    current_section_acronym = st_section_acronym
                    section = Section.objects.get(acronym=current_section_acronym)
                    student = self.update_and_get_student(sciper=current_sciper, username=xstr(st[6]))
                elif current_section_acronym != st_section_acronym:
                    current_section_acronym = st_section_acronym
                    section = Section.objects.get(acronym=current_section_acronym)
                if 'Rallonge' in st[5]:
                    to_save.append(Transaction(transaction_type='FACULTY_ALLOWANCE',
                                            transaction_date=st[2],
                                            amount=st[3],
                                            student=student,
                                            section=section,
                                            semester=semester))
                elif 'Allocation myPrint' in st[5]:
                    to_save.append(Transaction(transaction_type='MYPRINT_ALLOWANCE',
                                            transaction_date=st[2],
                                            amount=st[3],
                                            student=student,
                                            section=section,
                                            semester=semester))
                else:
                    raise ValueError('Type de transaction inconnue')
        Transaction.objects.bulk_create(to_save)
        to_save = []
        i = 0
        current_semester = None
        previous_semester = None
        for semester in Semester.objects.all().order_by('end_date'):
            i += 1
            print('Semester: {}'.format(i))
            previous_semester = current_semester
            if not current_semester:
                current_semester = semester
                semester_transactions = TAllTransactions.objects.filter(trans_datetime__lte=current_semester.end_date)
            else:
                current_semester = semester
                semester_transactions = TAllTransactions.objects.filter(trans_datetime__lte=current_semester.end_date,
                                                                        trans_datetime__gt=previous_semester.end_date)

            semester_transactions = semester_transactions.filter(hierarchie2='EPFL ETU').exclude(trans_origin='T_STUD_ALLOWANCE')
            semester_transactions = semester_transactions.exclude(Q(hierarchie3__icontains='audit') |
                                                                  Q(hierarchie3__icontains='EDOC'))
            semester_transactions = semester_transactions.values_list('person_sciper',
                                                                      'hierarchie3',
                                                                      'trans_datetime',
                                                                      'trans_amount',
                                                                      'trans_origin',
                                                                      'trans_description',
                                                                      'account_name')
            semester_transactions = semester_transactions.order_by('person_sciper', 'trans_datetime')

            current_sciper = ''
            current_section_acronym = ''
            student_total_spent = 0
            student_total_charged = 0
            last_transaction=None
            for st in semester_transactions:
                st_section_acronym = re.search('EPFL ETU (.*)-.*', st[1]).group(1)
                if not current_sciper:
                    current_sciper = st[0]
                if not current_section_acronym:
                    current_section_acronym = st_section_acronym
                if current_sciper != st[0]:
                    section = Section.objects.get(acronym=current_section_acronym)
                    student = self.update_and_get_student(sciper=current_sciper, username=xstr(last_transaction[6]))
                    if student_total_spent != 0:
                        to_save.append(Transaction(transaction_type='PRINT_JOB',
                                            transaction_date=last_transaction[2],
                                            amount=student_total_spent,
                                            student=student,
                                            section=section,
                                            semester=semester))
                    current_sciper = st[0]
                    current_section_acronym = st_section_acronym
                    student_total_spent = 0
                    student_total_charged = 0
                elif current_section_acronym != st_section_acronym:
                    section = Section.objects.get(acronym=current_section_acronym)
                    student = self.update_and_get_student(sciper=current_sciper, username=xstr(last_transaction[6]))
                    if student_total_spent != 0:
                        to_save.append(Transaction(transaction_type='PRINT_JOB',
                                            transaction_date=last_transaction[2],
                                            amount=student_total_spent,
                                            student=student,
                                            section=section,
                                            semester=semester))
                    current_section_acronym = st_section_acronym
                    student_total_spent = 0
                    student_total_charged = 0

                elif st[4] == 'T_ACCOUNT_CHARGING':
                    section = Section.objects.get(acronym=current_section_acronym)
                    student = self.update_and_get_student(sciper=current_sciper, username=xstr(st[6]))
                    to_save.append(Transaction(transaction_type='ACCOUNT_CHARGING',
                                            transaction_date=st[2],
                                            amount=st[3],
                                            student=student,
                                            section=section,
                                            semester=semester))
                    student_total_charged += st[3]
                elif st[4] == 'T_JOB_PROPS':
                    student_total_spent += st[3]
                last_transaction = st
            print('Saving transactions')
            Transaction.objects.bulk_create(to_save)
            to_save = []

        doubles = Transaction.objects.filter(transaction_type='MYPRINT_ALLOWANCE')
        doubles = doubles.values('semester', 'section', 'student', 'amount', 'transaction_date').annotate(total=Count('id'))
        doubles = doubles.order_by().filter(total__gt=1)
        for d in doubles:
            res = Transaction.objects.filter(semester__id=d['semester'],
                                             section__id=d['section'],
                                             student__id=d['student'],
                                             amount=d['amount'],
                                             transaction_date=d['transaction_date'])
            res[0].delete()

        semester_summaries = {}
        i = 0
        for transaction in Transaction.objects.all():
            i = i + 1
            if i % 10000 == 0:
                print(i)
            semester = transaction.semester
            student = transaction.student
            section = transaction.section
            if transaction.semester not in semester_summaries:
                semester_summaries[semester] = {}
            if transaction.section not in semester_summaries[semester]:
                semester_summaries[semester][section] = {}
            if transaction.student not in semester_summaries[semester][section]:
                semester_summaries[semester][section][student] = SemesterSummary(semester=semester, section=section, student=student)

            if transaction.transaction_type == 'MYPRINT_ALLOWANCE':
                semester_summaries[semester][section][student].myprint_allowance += transaction.amount
            elif transaction.transaction_type == 'ACCOUNT_CHARGING':
                semester_summaries[semester][section][student].total_charged += transaction.amount
            elif transaction.transaction_type == 'FACULTY_ALLOWANCE':
                semester_summaries[semester][section][student].faculty_allowance += transaction.amount
            elif transaction.transaction_type == 'PRINT_JOB' or transaction.transaction_type == 'REFUND':
                semester_summaries[semester][section][student].total_spent += transaction.amount

        semester_summaries_arr = []
        for semester, dict1 in semester_summaries.items():
            for section, dict2 in dict1.items():
                for student, value in dict2.items():
                    semester_summaries_arr.append(value)
        SemesterSummary.objects.bulk_create(semester_summaries_arr)
