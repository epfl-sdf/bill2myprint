import json
from collections import defaultdict
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Count, Sum, Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Custom models
from uniflow.models import BudgettransactionsT
from bill2myprint.models import *



##########################
#
# LOCAL FUNCTIONS
#
##########################

def __get_semesters():
    return Semester.objects.order_by("end_date").values_list('name', flat=True)


def __get_faculties():
    return SemesterSummary.objects.\
        order_by("section__faculty__name"). \
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
            order_by("end_date"). \
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


def __compute(dict):
    return min(0, dict['vpsi'] + dict['added'] + dict['spent'] - dict['amount'])


##########################
#
# FUNCTIONS FROM VIEWS
#
##########################

def compute_all(request):
    # Semesters must be ordered to compute facturation historically
    semesters = __get_semesters()
    sections = Section.objects.all()
    students = Student.objects.all()

    for section in sections:
        for student in students:
            dict = defaultdict(float)
            for semester in semesters:
                semesters_data = SemesterSummary.objects.\
                    filter(semester__name=semester).\
                    filter(section=section).\
                    filter(student=student)
                if semesters_data:
                    dict['vpsi'] += semesters_data[0].myprint_allowance
                    dict['faculty'] += semesters_data[0].faculty_allowance
                    dict['added'] += semesters_data[0].total_charged
                    dict['spent'] += semesters_data[0].total_spent
                    semesters_data[0].facturation_faculty = __compute(dict)
                    semesters_data[0].save()
                    dict['amount'] += semesters_data[0].facturation_faculty

    return HttpResponseRedirect(reverse('homepage'))


def compute(request, semester):
    # Semesters must be ordered to compute facturation historically
    semesters = __get_semesters()
    sections = Section.objects.all()
    students = Student.objects.filter(semestersummary__semester__name=semester)

    for section in sections:
        for student in students:
            dict = defaultdict(float)
            for semester in semesters:
                semesters_data = SemesterSummary.objects. \
                    filter(semester__name=semester). \
                    filter(section=section). \
                    filter(student=student)
                if semesters_data:
                    dict['vpsi'] += semesters_data[0].myprint_allowance
                    dict['faculty'] += semesters_data[0].faculty_allowance
                    dict['added'] += semesters_data[0].total_charged
                    dict['spent'] += semesters_data[0].total_spent
                    semesters_data[0].facturation_faculty = __compute(dict)
                    semesters_data[0].save()
                    dict['amount'] += semesters_data[0].facturation_faculty

    return HttpResponseRedirect(reverse('homepage'))


##########################
#
# VIEWS FUNCTIONS
#
##########################

def homepage(request):
    semesters = __get_semesters()
    current_semester = __get_current_semester(request.POST)

    faculties = SemesterSummary.objects.\
        filter(semester__name=current_semester).\
        order_by("section__faculty__name").\
        values('section__faculty__name').\
        annotate(amount=Sum('facturation_faculty'))

    number_of_students = __get_number_of_students(semester=current_semester)

    last_update = UpdateStatus.objects.latest(field_name="update_date")

    return render(
        request,
        'bill2myprint/homepage.html',
        {
            'is_homepage': True,
            'current_semester': current_semester,
            'semesters': semesters,
            'faculties': faculties,
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
            dict['amount'] = section_data.aggregate(Sum('facturation_faculty'))['facturation_faculty__sum']
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
        filter(section__acronym=current_section). \
        order_by("student__sciper"). \
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
        ## Trying to sort the whole transaction set, rather than just the current page
        ## Need to implement special function ?
        #attr = request.POST.get('attr')
        #if attr:
        #    if request.POST.get('attr') == 'date':
        #        transactions = transactions.order_by("-transaction_date") if request.POST.get('order') == 'desc' else transactions.order_by("transaction_date")
        #    elif attr and request.POST.get('attr') == 'semester':
        #        transactions = transactions.order_by("-semester__name") if request.POST.get('order') == 'desc' else transactions.order_by("semester__name")
        #    elif attr and request.POST.get('attr') == 'type':
        #        transactions = transactions.order_by("-transaction_type") if request.POST.get('order') == 'desc' else transactions.order_by("transaction_type")
        #    elif attr and request.POST.get('attr') == 'amount':
        #        transactions = transactions.order_by("-amount") if request.POST.get('order') == 'desc' else transactions.order_by("amount")

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
    status_table= UpdateStatus.objects.order_by("-update_date")

    return render(
        request,
        'bill2myprint/status.html',
        {
            'is_miscellaneous': True,
            'status_table': status_table,
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
        students = Student.objects. \
            filter(Q(**{"name__istartswith": pattern}) | Q(**{"name__icontains": ' ' + pattern})). \
            extra(select={'student': 'name'})

    return HttpResponse(json.dumps(list(students.order_by('student').values('student'))))
