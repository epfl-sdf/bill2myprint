import re
import gc
from datetime import timedelta

from django.core.management.base import BaseCommand

from bill2myprint.models import Student, Semester, Transaction, Section, SemesterSummary, OurCatTransaction, VPersonDeltaHistory, OurCatValidation, CasTrxAccExt


def xstr(s):
    if s is None:
        return ''
    return s


class Command(BaseCommand):
    help = 'Populates the database with sections and the faculties'

    def update_and_get_student(self, sciper, username):
        student = Student.objects.get_or_create(sciper=sciper)[0]
        if username and student.username != username:
            student.username = username
            student.save()
        return student

    def handle_first_uniflow_allowance(self, student, section):
        semester = Semester.objects.get(name='Automne 2016-2017')
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
            student.has_uniflow_initial_allowance = True
            student.save()

    def handle(self, *args, **options):
        consolidated_data = {}
        received_my_print_allow = {}
        first_uniflow_semester = Semester.objects.get(name='Automne 2016-2017')
        cdm_last_allowance_semester = Semester.objects.get(name='Automne 2012-2013')
        first_semester = Semester.objects.order_by('end_date')[0]
        charg_regex = re.compile(".*c.*arg.*")

        transactions = OurCatTransaction.objects.order_by('pk')
        last_pk = OurCatTransaction.objects.order_by('-pk')[0].pk
        pk = 0
        while pk < last_pk:
            print(pk)
            for trans in transactions.filter(pk__gt=pk)[:5000]:
                pk = trans.pk
                try:
                    equitrac_user = OurCatValidation.objects.get(id=trans.chargeid)
                except OurCatValidation.DoesNotExist:
                    continue
                if equitrac_user.valtype != 'usr':
                    continue
                infos = VPersonDeltaHistory.get_infos_for_equitrac(username=equitrac_user.name, time=trans.trxdate)
                if infos is None:
                    continue
                sciper = infos['sciper']
                if not infos['is_student']:
                    continue
                student = self.update_and_get_student(sciper=sciper, username=equitrac_user.name)
                section_acronym = infos['section_acronym']
                try:
                    section = Section.objects.get(acronym=section_acronym)
                except Section.DoesNotExist:
                    continue
                if trans.trxtype == 'acc':
                    trx_details = CasTrxAccExt.objects.get(x_id=pk)
                    if trans.amount <= -100 or trans.amount >= 1000:
                        continue
                    if not float(trans.amount).is_integer():
                        transaction_type = 'REFUND'
                        semester = Semester.objects.filter(end_date__gte=trans.trxdate).order_by('end_date')[0]
                    elif 'acctcharge' in trx_details.operatorname.lower() or charg_regex.match(trx_details.details.lower()) or \
                            (trx_details.details and 'transaction #' in trx_details.details.lower()):
                        transaction_type = 'ACCOUNT_CHARGING'
                        semester = Semester.objects.filter(end_date__gte=trans.trxdate).order_by('end_date')[0]
                    elif trans.trxdate < first_semester.end_date_official:
                        semester = Semester.objects.filter(end_date_official__gte=trans.trxdate).order_by('end_date_official')[0]
                        transaction_type = 'MYPRINT_ALLOWANCE'
                    elif trx_details.details and 'ajustement' in trx_details.details.lower():
                        transaction_type = 'MYPRINT_ALLOWANCE'
                        semester = Semester.objects.filter(end_date_official__gte=trans.trxdate).order_by('end_date_official')[0]
                    elif trx_details.details and trx_details.details.lower() == 'initial account balance':
                        semester = Semester.objects.filter(end_date_official__gte=trans.trxdate).order_by('end_date_official')[0]
                        transaction_type = 'MYPRINT_ALLOWANCE'
                        if sciper not in received_my_print_allow:
                            received_my_print_allow[sciper] = {}
                        if semester.id not in received_my_print_allow[sciper]:
                            received_my_print_allow[sciper][semester.id] = True
                            transaction_type = 'MYPRINT_ALLOWANCE'
                    else:
                        semester = Semester.objects.filter(end_date_official__gte=trans.trxdate).order_by('end_date_official')[0]
                        if trans.amount == 24:
                            if sciper not in received_my_print_allow:
                                received_my_print_allow[sciper] = {}
                            if semester.id not in received_my_print_allow[sciper]:
                                received_my_print_allow[sciper][semester.id] = True
                                transaction_type = 'MYPRINT_ALLOWANCE'
                            elif received_my_print_allow[sciper][semester.id]:
                                transaction_type = 'FACULTY_ALLOWANCE'
                        else:
                            transaction_type = 'FACULTY_ALLOWANCE'
                    if transaction_type == 'FACULTY_ALLOWANCE':
                        if abs(trans.amount) not in [12, 16, 24, 26, 32, 50]:
                            transaction_type = 'REFUND'
                            semester = Semester.objects.filter(end_date__gte=trans.trxdate).order_by('end_date')[0]
                        else:
                            if section.faculty.name not in ['CDM', 'ENAC', 'SV', 'SB']:
                                transaction_type = 'MYPRINT_ALLOWANCE'
                                semester = Semester.objects.filter(end_date_official__gte=trans.trxdate).order_by('end_date')[0]
                            else:
                                if section.faculty.name == 'CDM':
                                    if trans.trxdate > cdm_last_allowance_semester.end_date_official:
                                        transaction_type = 'MYPRINT_ALLOWANCE'
                                        semester = Semester.objects.filter(end_date_official__gte=trans.trxdate).order_by('end_date')[0]
                elif trans.trxtype == 'doc':
                    semester = Semester.objects.filter(end_date__gte=trans.trxdate).order_by('end_date')[0]
                    transaction_type = 'PRINT_JOB'
                else:
                    continue
                if semester.end_date >= first_uniflow_semester.end_date:
                    self.handle_first_uniflow_allowance(student=student, section=section)
                if section != student.last_known_section:
                    student.last_known_section = section
                    student.save()
                if semester.id not in consolidated_data:
                    consolidated_data[semester.id] = {}
                if sciper not in consolidated_data[semester.id]:
                    consolidated_data[semester.id][sciper] = {}
                if section.id not in consolidated_data[semester.id][sciper]:
                    consolidated_data[semester.id][sciper][section.id] = {}
                if transaction_type not in consolidated_data[semester.id][sciper][section.id]:
                    consolidated_data[semester.id][sciper][section.id][transaction_type] = 0
                consolidated_data[semester.id][sciper][section.id][transaction_type] += trans.amount
            gc.collect()

        transactions = []
        for semester_id, dict1 in consolidated_data.items():
            for sciper, dict2 in dict1.items():
                for section_id, dict3 in dict2.items():
                    for transaction_type, amount in dict3.items():
                        semester = Semester.objects.get(id=semester_id)
                        if semester_id == 15:
                            previous_id = semester_id - 1
                            previous_semester = Semester.objects.get(id=previous_id)
                            dt = previous_semester.end_date + timedelta(days=1)
                        else:
                            dt = semester.end_date_official - timedelta(days=1)
                        student = Student.objects.get(sciper=sciper)
                        section = Section.objects.get(id=section_id)
                        Transaction.objects.create(transaction_type=transaction_type,
                                                   transaction_date=dt,
                                                   amount=amount,
                                                   student=student,
                                                   section=section,
                                                   semester=semester)

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
