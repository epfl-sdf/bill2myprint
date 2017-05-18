import re

from django.db.models import Q
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
        to_save_compacted = []
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

            semester_transactions = semester_transactions.filter(hierarchie2='EPFL ETU')
            semester_transactions = semester_transactions.exclude(Q(hierarchie3__icontains='audit') |
                                                                  Q(hierarchie3__icontains='EDOC'))
            semester_transactions = semester_transactions.values_list('person_sciper',
                                                                      'hierarchie3',
                                                                      'trans_datetime',
                                                                      'trans_amount',
                                                                      'trans_origin',
                                                                      'trans_description',
                                                                      'account_name')
            semester_transactions = semester_transactions.order_by('person_sciper')

            current_sciper = ''
            current_section_acronym = ''
            student_total_spent = 0
            student_total_charged = 0
            student_fac_allowance = 0
            student_myprint_allowance = 0
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
                    to_save_compacted.append(SemesterSummary(student=student,
                                                             semester=semester,
                                                             total_charged=student_total_charged,
                                                             total_spent=student_total_spent,
                                                             myprint_allowance=student_myprint_allowance,
                                                             faculty_allowance=student_fac_allowance,
                                                             section=section)
                                             )
                    current_sciper = st[0]
                    current_section_acronym = st_section_acronym
                    student_total_spent = 0
                    student_total_charged = 0
                    student_fac_allowance = 0
                    student_myprint_allowance = 0
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
                    to_save_compacted.append(SemesterSummary(student=student,
                                                             semester=semester,
                                                             total_charged=student_total_charged,
                                                             total_spent=student_total_spent,
                                                             myprint_allowance=student_myprint_allowance,
                                                             faculty_allowance=student_fac_allowance,
                                                             section=section)
                                             )
                    current_section_acronym = st_section_acronym
                    student_total_spent = 0
                    student_total_charged = 0
                    student_fac_allowance = 0
                    student_myprint_allowance = 0

                if st[4] == 'T_STUD_ALLOWANCE':
                    student = self.update_and_get_student(sciper=current_sciper, username=xstr(st[6]))
                    section = Section.objects.get(acronym=current_section_acronym)
                    if 'Rallonge' in st[5]:
                        to_save.append(Transaction(transaction_type='FACULTY_ALLOWANCE',
                                                transaction_date=st[2],
                                                amount=st[3],
                                                student=student,
                                                section=section,
                                                semester=semester))
                        student_fac_allowance += st[3]
                    elif 'Allocation myPrint' in st[5]:
                        to_save.append(Transaction(transaction_type='MYPRINT_ALLOWANCE',
                                                transaction_date=st[2],
                                                amount=st[3],
                                                student=student,
                                                section=section,
                                                semester=semester))
                        student_myprint_allowance += st[3]
                    else:
                        raise ValueError('Type de transaction inconnue')
                elif st[4] == 'T_ACCOUNT_CHARGING':
                    student = self.update_and_get_student(sciper=current_sciper, username=xstr(st[6]))
                    section = Section.objects.get(acronym=current_section_acronym)
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
            SemesterSummary.objects.bulk_create(to_save_compacted)
            to_save_compacted = []
