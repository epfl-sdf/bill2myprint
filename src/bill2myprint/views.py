# -*- coding:utf-8 -*-

"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""

import json
import ast
from collections import defaultdict, OrderedDict
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum, Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Custom models
from uniflow.models import BudgettransactionsT
from .models import Section, Semester, SemesterSummary, Student, Transaction, UpdateStatus


##########################
#
# LOCAL FUNCTIONS
#
##########################


def __get_semesters():
    return Semester.objects.order_by("end_date").values_list('name', flat=True)


def __get_faculties():
    return SemesterSummary.objects.\
        order_by("section__faculty__name").\
        values_list('section__faculty__name', flat=True).\
        distinct()


def __get_sections_by_faculty(faculty):
    return SemesterSummary.objects.\
        filter(section__faculty__name=faculty).\
        order_by("section__acronym").\
        values_list('section__acronym', flat=True).\
        distinct()


def __get_current_faculty(faculties, post, arg):
    return arg if arg else post['faculty'] if 'faculty' in post else faculties[0]


def __get_current_semester(post, arg=""):
    if arg:
        semester = arg
    elif 'semester' in post:
        semester = post['semester']
    else:
        now = datetime.now()
        semesters = Semester.objects.\
            filter(end_date__gt=now).\
            order_by("end_date").\
            values_list('name', flat=True)
        semester = semesters[0]

    return semester


def __get_number_of_students(semester, faculty="", section=""):
    number_of_students = SemesterSummary.objects.filter(semester__name=semester)
    if faculty:
        number_of_students = number_of_students.filter(section__faculty__name=faculty)
    if section:
        number_of_students = number_of_students.filter(section__acronym=section)
    return number_of_students.values('student').distinct().count()


def __get_floored_faculties_allowance(floors, amount, charges):
    result = defaultdict(float)
    prev_floor = 0
    for floor in floors:
        if prev_floor <= amount <= floor[1]:
            new_amount = min(floor[1], amount + charges)
            if new_amount != amount:
                result[floor[0]] += new_amount - amount
            charges = max(0, amount + charges - floor[1])
            amount = new_amount
        prev_floor = floor[1]
    return result


def __compute(dict):
    return min(0, dict['vpsi'] + dict['added'] + dict['spent'] - dict['amount'])


def __compute_bill(semester, faculty, section=""):
    fac_sect = faculty + ":" + section

    billing_faculty = SemesterSummary.objects.\
        filter(semester__name=semester).\
        filter(billing_faculty__contains=fac_sect).\
        values_list('billing_faculty', flat=True)

    sum_bill = 0.0
    for bill in billing_faculty:
        bill_dict = ast.literal_eval(bill)
        for key, value in bill_dict.items():
            if fac_sect in key:
                sum_bill += value
    return sum_bill


##########################
#
# FUNCTIONS FROM VIEWS
#
##########################


def compute(request, semester=""):
    # Semesters must be ordered to compute billing historically
    semesters = __get_semesters()

    students = Student.objects.all()

    if semester:
        students = students.filter(semestersummary__semester__name=semester)

    for student in students:
        comp_dict = defaultdict(float)
        floored_faculty_allowance = []
        for t_semester in semesters:
            semesters_datas = SemesterSummary.objects.\
                filter(semester__name=t_semester).\
                filter(student=student).\
                order_by("-myprint_allowance", "-faculty_allowance")
            for semesters_data in semesters_datas:
                comp_dict['vpsi'] += semesters_data.myprint_allowance
                comp_dict['faculty'] += semesters_data.faculty_allowance
                comp_dict['added'] += semesters_data.total_charged
                comp_dict['spent'] += semesters_data.total_spent

                total_billing_faculties = __compute(comp_dict)

                section = Section.objects.get(id=semesters_data.section_id)
                floored_faculty_allowance.append([section.faculty.name + ":" + section.acronym, comp_dict['faculty']])

                faculties_billing = __get_floored_faculties_allowance(
                    floored_faculty_allowance,
                    -comp_dict['amount'],
                    -total_billing_faculties
                )

                if not semester or t_semester == semester:
                    semesters_data.billing_faculty = repr(dict(faculties_billing))
                    semesters_data.save()

                comp_dict['billing_faculty'] = -sum(faculties_billing.values())
                comp_dict['amount'] += comp_dict['billing_faculty']

            if semester and t_semester == semester:
                break

    return HttpResponseRedirect(reverse('homepage'))


##########################
#
# VIEWS FUNCTIONS
#
##########################

def homepage(request):
    semesters = __get_semesters()
    current_semester = __get_current_semester(request.POST)
    faculties = __get_faculties()

    billing = dict()
    for faculty in faculties:
        billing[faculty] = __compute_bill(semester=current_semester, faculty=faculty)

    number_of_students = __get_number_of_students(semester=current_semester)

    last_update = UpdateStatus.objects.latest(field_name="update_date")

    return render(
        request,
        'bill2myprint/homepage.html',
        {
            'is_homepage': True,
            'current_semester': current_semester,
            'semesters': semesters,
            'faculties': OrderedDict(sorted(billing.items())),
            'last_update': last_update,
            'number_of_students': number_of_students,
        }
    )


def faculties(request, faculty="", semester=""):
    semesters = __get_semesters()
    faculties = __get_faculties()
    current_semester = __get_current_semester(post=request.POST, arg=semester)
    current_faculty = __get_current_faculty(faculties=faculties, post=request.POST, arg=faculty)
    sections = __get_sections_by_faculty(current_faculty)

    semesters_data = SemesterSummary.objects.filter(semester__name=current_semester)

    sections_data = []
    for section in sections:
        section_data = semesters_data.filter(section__acronym=section)
        dict = defaultdict(float)
        dict['section'] = section
        if section_data:
            dict['vpsi'] = section_data.aggregate(Sum('myprint_allowance'))['myprint_allowance__sum']
            dict['faculty'] = section_data.aggregate(Sum('faculty_allowance'))['faculty_allowance__sum']
            dict['added'] = section_data.aggregate(Sum('total_charged'))['total_charged__sum']
            dict['spent'] = section_data.aggregate(Sum('total_spent'))['total_spent__sum']
            dict['amount'] = __compute_bill(semester=current_semester, faculty=current_faculty, section=section)
        sections_data.append(dict)

    number_of_students = __get_number_of_students(semester=current_semester, faculty=current_faculty)

    return render(
        request,
        'bill2myprint/faculties.html',
        {
            'is_faculties': True,
            'faculties': faculties,
            'sections': sections,
            'semesters': semesters,
            'current_faculty': current_faculty,
            'current_semester': current_semester,
            'number_of_students': number_of_students,
            'sections_data': sections_data,
        }
    )


def sections(request, faculty="", section="", semester=""):
    semesters = __get_semesters()
    faculties = __get_faculties()
    current_semester = __get_current_semester(post=request.POST, arg=semester)
    current_faculty = __get_current_faculty(faculties=faculties, post=request.POST, arg=faculty)
    sections = __get_sections_by_faculty(current_faculty)

    current_section = sections[0]
    if section:
        current_section = section
    elif ('section' in request.POST) and (request.POST['section'] in sections):
            current_section = request.POST['section']

    students = SemesterSummary.objects.\
        filter(semester__name=current_semester).\
        filter(section__acronym=current_section).\
        order_by("student__sciper").\
        values('student__sciper',
               'myprint_allowance',
               'faculty_allowance',
               'total_charged',
               'total_spent')

    number_of_students = len(students)

    paginator = Paginator(students, 50)
    page = request.GET.get('page')
    try:
        students_p = paginator.page(page)
    except PageNotAnInteger:
        students_p = paginator.page(1)
    except EmptyPage:
        students_p = paginator.page(paginator.num_pages)

    return render(
        request,
        'bill2myprint/sections.html',
        {
            'is_sections': True,
            'faculties': faculties,
            'sections': sections,
            'semesters': semesters,
            'current_faculty': current_faculty,
            'current_section': current_section,
            'current_semester': current_semester,
            'number_of_students': number_of_students,
            'students': students_p,
        }
    )


def students(request, sciper=""):

    if 'student' in request.POST:
        if request.POST['student'].isdigit():
            student_sciper = request.POST['student']
            student_name = None
        else:
            student_sciper = None
            student_name = request.POST['student']
    elif sciper:
        student_sciper = sciper
        student_name = None
    else:
        student_sciper = None
        student_name = None

    if student_sciper:
        try:
            student = Student.objects.get(sciper=student_sciper)
        except ObjectDoesNotExist:
            student = None

        transactions = Transaction.objects.filter(student__sciper=student_sciper)

    elif student_name:
        try:
            student = Student.objects.get(name=student_name)
        except ObjectDoesNotExist:
            student = None

        transactions = Transaction.objects.filter(student__name=student_name)

    else:
        student = None
        transactions = None

    if transactions:
        cumulated = list(transactions.values('transaction_type').annotate(Sum('amount')))
        transactions = transactions.order_by("-transaction_date")
    else:
        cumulated = None

    t = defaultdict(float)
    if cumulated:
        for cumulus in cumulated:
            if cumulus['transaction_type'] == 'MYPRINT_ALLOWANCE':
                t['vpsi'] = cumulus['amount__sum']
            if cumulus['transaction_type'] == 'FACULTY_ALLOWANCE':
                t['faculty'] = cumulus['amount__sum']
            if cumulus['transaction_type'] == 'ACCOUNT_CHARGING':
                t['added'] = cumulus['amount__sum']
            if cumulus['transaction_type'] == 'PRINT_JOB':
                t['spent'] = t['spent'] + cumulus['amount__sum']
            if cumulus['transaction_type'] == 'REFUND':
                t['spent'] = t['spent'] + cumulus['amount__sum']
        t['credit'] = t['vpsi'] + t['faculty'] + t['added'] + t['spent']

    paginator = Paginator(transactions, 50)
    page = request.GET.get('page')
    if transactions:
        try:
            transactions_p = paginator.page(page)
        except PageNotAnInteger:
            transactions_p = paginator.page(1)
        except EmptyPage:
            transactions_p = paginator.page(paginator.num_pages)
    else:
        transactions_p = None

    return render(
        request,
        'bill2myprint/students.html',
        {
            'is_students': True,
            'student': student,
            'transactions': transactions_p,
            'cumulated': t,
        }
    )


def faculty_extension(request):

    transactions = BudgettransactionsT.objects.\
        filter(transactiondata__startswith='Rallonge').\
        distinct().\
        values_list('transactiondata')

    faculties = __get_faculties()

    faculties_extensions = []

    for faculty in faculties:
        sections = __get_sections_by_faculty(faculty)
        for section in sections:
            for transaction in transactions:
                if len(transaction) == 0:
                    continue
                keys = transaction[0].split(" ")
                dict = {}
                found = False
                for key in keys:
                    if "_StudU" in key:
                        if key.startswith(section):
                            dict["faculty"] = faculty
                            dict["section"] = section
                            dict["entity"] = key.replace("_StudU", "")[len(section):]
                            dict["whole_entity"] = key
                            found = True
                    elif found and key.isdigit():
                        dict["amount"] = key
                if found:
                    faculties_extensions.append(dict)

    faculties_extensions = sorted(faculties_extensions, key=lambda k: (k['faculty'], k['whole_entity']))

    return render(
        request,
        'bill2myprint/faculty_extension.html',
        {
            'is_miscellaneous': True,
            'faculties_extensions': faculties_extensions,
        }
    )


def status(request):
    status_table = UpdateStatus.objects.order_by("-update_date")

    return render(
        request,
        'bill2myprint/status.html',
        {
            'is_miscellaneous': True,
            'status_table': status_table,
        }
    )


def student_billing(request):
    message = ""
    transactions = []
    student = None

    if "student" in request.POST:
        sciper = request.POST['student']
        students = Student.objects.filter(sciper=sciper)

        if len(students) > 0:
            student = students[0]
            semesters = __get_semesters()
            comp_dict = defaultdict(float)
            floored_faculty_allowance = []
            for semester in semesters:
                semesters_datas = SemesterSummary.objects.\
                    filter(semester__name=semester).\
                    filter(student=student).\
                    order_by("-myprint_allowance", "-faculty_allowance").\
                    values()
                for semesters_data in semesters_datas:
                    comp_dict['vpsi'] += semesters_data['myprint_allowance']
                    comp_dict['faculty'] += semesters_data['faculty_allowance']
                    comp_dict['added'] += semesters_data['total_charged']
                    comp_dict['spent'] += semesters_data['total_spent']
                    comp_dict['billing_faculty'] = __compute(comp_dict)

                    section = Section.objects.get(id=semesters_data['section_id'])
                    floored_faculty_allowance.append(
                        [section.faculty.name + ":" + section.acronym, comp_dict['faculty']]
                    )

                    facs_billing = __get_floored_faculties_allowance(
                        floored_faculty_allowance,
                        -comp_dict['amount'],
                        -comp_dict['billing_faculty']
                    )

                    comp_dict['billing_faculty'] = -sum(facs_billing.values())
                    comp_dict['amount'] += comp_dict['billing_faculty']

                    trans_dict = dict()
                    trans_dict['semester'] = semester
                    trans_dict['faculty_name'] = section.faculty.name
                    trans_dict['facs_billing'] = dict(facs_billing)
                    trans_dict['vpsi'] = semesters_data['myprint_allowance']
                    trans_dict['faculty'] = semesters_data['faculty_allowance']
                    trans_dict['added'] = semesters_data['total_charged']
                    trans_dict['spent'] = semesters_data['total_spent']
                    trans_dict['cum_vpsi'] = comp_dict['vpsi']
                    trans_dict['cum_faculty'] = comp_dict['faculty']
                    trans_dict['cum_added'] = comp_dict['added']
                    trans_dict['cum_spent'] = comp_dict['spent']
                    trans_dict['cum_amount'] = comp_dict['amount']
                    trans_dict['billing'] = comp_dict['billing_faculty']
                    transactions.append(trans_dict)
        else:
            message = "Numéro sciper invalide"

    return render(
        request,
        'bill2myprint/student_billing.html',
        {
            'is_miscellaneous': True,
            'student': student,
            'transactions': transactions,
            'message': message,
        }
    )


##########################
#
# AJAX FUNCTIONS
#
##########################


def sciper_list(request):
    pattern = request.GET.get('term', None)

    if pattern.isdigit():
        students = Student.objects.\
            filter(sciper__icontains=pattern). \
            extra(select={'student': 'sciper'})
    else:
        students = Student.objects.\
            filter(Q(**{"name__istartswith": pattern}) | Q(**{"name__icontains": ' ' + pattern})).\
            extra(select={'student': 'name'})

    return HttpResponse(json.dumps(list(students.order_by('student').values('student'))))
