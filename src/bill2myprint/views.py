# -*- coding:utf-8 -*-

"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""

import json
import ast
import locale
from collections import defaultdict, OrderedDict
from datetime import datetime, timedelta
from fpdf import FPDF

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum, Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

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


def __set_pagination(objects, items_per_page, page):
    paginator = Paginator(objects, items_per_page)
    try:
        pagin = paginator.page(page)
    except PageNotAnInteger:
        pagin = paginator.page(1)
    except EmptyPage:
        pagin = paginator.page(paginator.num_pages)

    index = pagin.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    return {'objects': pagin, 'page_range': page_range}


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


def __create_PDF(faculty, date_start, date_end, data, total):
    title = u"Facturation myPrint étudiants " + faculty
    subtitle1 = "Consommation des rallonges facultaires"
    subtitle2 = u"période du " + date_start + " au " + date_end

    class PDF(FPDF):
        def __init__(self):
            FPDF.__init__(self)
            self.add_font('DejaVu-Bold', '', 'DejaVuSansCondensed-Bold.ttf', uni=True)
            self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
            self.set_margins(20, 20, 20)

        def header(self):
            # Logo
            # self.image('logo_pb.png', 10, 8, 33)

            # title
            self.set_font('DejaVu-Bold', '', 15)
            w = self.get_string_width(title) + 6
            self.set_x((210 - w) / 2)
            self.cell(w, 9, title, 0, 0, 'C', 0)
            self.ln(15)

            # subtitle1
            self.set_font('DejaVu', '', 13)
            w = self.get_string_width(subtitle1) + 6
            self.set_x((210 - w) / 2)
            self.set_text_color(0, 128, 254)
            self.cell(w, 9, subtitle1, 0, 0, 'C')
            self.ln(7)

            # subtitle2
            w = self.get_string_width(subtitle2) + 6
            self.set_x((210 - w) / 2)
            self.set_text_color(0, 128, 254)
            self.cell(w, 9, subtitle2, 0, 0, 'C')
            self.ln(15)

            # line
            self.set_draw_color(0, 128, 254)
            self.set_fill_color(0, 128, 254)
            self.cell(0, 1, "", 1, 0, "", 1)
            self.ln(15)

        # Page footer
        def footer(self):
            pdf.set_font('DejaVu', '', 12)
            pdf.set_text_color(0, 0, 0)
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    section_margin = 40;
    semester_margin = 90
    amount_margin = 40

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_font('DejaVu-Bold', '', 12)
    pdf.cell(section_margin, 0, "Section", 0, 0)
    pdf.cell(semester_margin, 0, "Semestre", 0, 0)
    pdf.cell(amount_margin, 0, "Consommation", 0, 1, 'R')
    pdf.ln(10)

    pdf.set_font('DejaVu', '', 12)

    section = data[0]['section']
    for datum in data:
        if datum['section'] != section:
            section = datum['section']
            pdf.ln(15)
        else:
            pdf.ln(7)
        pdf.cell(section_margin, 0, datum['section'], 0, 0)
        pdf.cell(semester_margin, 0, datum['semester'], 0, 0)
        pdf.cell(amount_margin, 0, locale.format('%.2f', datum['amount'], True), 0, 1, 'R')
    pdf.ln(20)

    pdf.set_font('DejaVu-Bold', '', 12)
    pdf.cell(section_margin, 0, "Total", 0, 0)
    pdf.cell(semester_margin, 0, "", 0, 0)
    pdf.set_text_color(254, 0, 0)
    pdf.cell(amount_margin, 0, locale.format('%.2f', total, True), 0, 1, 'R')

    pdf.output(settings.MEDIA_ROOT + 'pdf/Facturation-' + faculty + '.pdf', 'F')


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

            if not semester or t_semester == semester:
                comp_dict['remain'] = comp_dict['vpsi'] + comp_dict['faculty'] + comp_dict['added'] + comp_dict['spent']
                for semesters_data in semesters_datas:
                    semesters_data.remain = comp_dict['remain']
                    semesters_data.save()

            if semester and t_semester == semester:
                break

    return HttpResponseRedirect(reverse('homepage'))


##########################
#
# VIEWS FUNCTIONS
#
##########################

def homepage(request):
    locale.setlocale(locale.LC_NUMERIC, 'fr_CH.utf8')

    semesters = __get_semesters()
    current_semester = __get_current_semester(request.POST)
    faculties = __get_faculties()

    billing = dict()
    sum_billing = 0.0
    for faculty in faculties:
        billing[faculty] = __compute_bill(semester=current_semester, faculty=faculty)
        sum_billing += billing[faculty]

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
            'sum_billing': sum_billing,
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

    if 'faculty' in request.POST:
        kwargs = {'faculty': current_faculty, 'semester': current_semester}
        return HttpResponseRedirect(reverse('faculties', kwargs=kwargs))

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

    if 'faculty' in request.POST:
        faculty = request.POST['faculty']
        kwargs = {'faculty': faculty, 'section': current_section, 'semester': current_semester}
        return HttpResponseRedirect(reverse('sections', kwargs=kwargs))

    students = SemesterSummary.objects.\
        filter(semester__name=current_semester).\
        filter(section__acronym=current_section).\
        order_by("student__sciper").\
        values('student__sciper',
               'myprint_allowance',
               'faculty_allowance',
               'total_charged',
               'total_spent',
               'remain',
               'billing_faculty')

    pagination = __set_pagination(students, 50, request.GET.get('page'))

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
            'number_of_students': len(students),
            'students': pagination['objects'],
            'page_range': pagination['page_range'],
        }
    )


def students(request, sciper=""):
    if 'student' in request.POST:
        if request.POST['student'].isdigit():
            student_sciper = request.POST['student']
            return HttpResponseRedirect(reverse('students', kwargs={'sciper': student_sciper}))
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
            return HttpResponseRedirect(reverse('students', kwargs={'sciper': student.sciper}))
        except ObjectDoesNotExist:
            student = None

        transactions = Transaction.objects.filter(student__name=student_name)

    else:
        student = None
        transactions = []

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

    pagination = __set_pagination(transactions, 50, request.GET.get('page'))

    return render(
        request,
        'bill2myprint/students.html',
        {
            'is_students': True,
            'student': student,
            'transactions': pagination['objects'],
            'page_range': pagination['page_range'],
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
                        dict["amount"] = float(key)
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
                    comp_dict['remain'] = semesters_data['myprint_allowance'] +\
                                          semesters_data['faculty_allowance'] +\
                                          semesters_data['total_charged'] +\
                                          semesters_data['total_spent']
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
                    comp_dict['cum_remain'] += comp_dict['remain']

                    trans_dict = dict()
                    trans_dict['semester'] = semester
                    trans_dict['faculty_name'] = section.faculty.name
                    trans_dict['facs_billing'] = dict(facs_billing)
                    trans_dict['vpsi'] = semesters_data['myprint_allowance']
                    trans_dict['faculty'] = semesters_data['faculty_allowance']
                    trans_dict['added'] = semesters_data['total_charged']
                    trans_dict['spent'] = semesters_data['total_spent']
                    trans_dict['remain'] = comp_dict['remain']
                    trans_dict['cum_vpsi'] = comp_dict['vpsi']
                    trans_dict['cum_faculty'] = comp_dict['faculty']
                    trans_dict['cum_added'] = comp_dict['added']
                    trans_dict['cum_spent'] = comp_dict['spent']
                    trans_dict['cum_amount'] = comp_dict['amount']
                    trans_dict['cum_remain'] = comp_dict['cum_remain']
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


def download_faculty(request, faculty="", semester=""):
    all_semesters = list(__get_semesters())
    sections = __get_sections_by_faculty(faculty)

    if 'semesters' in request.POST:
        semesters_temp = request.POST.getlist('semesters')
    else:
        semesters_temp = []
        semesters_temp.append(semester)

    semesters = []
    for sem in all_semesters:
        if sem in semesters_temp:
            semesters.append(sem)

    date_start = datetime.strptime('01019999', '%d%m%Y').date()
    date_end = datetime.strptime('01010001', '%d%m%Y').date()
    for sem in semesters:
        curr_sem = Semester.objects.get(name=sem)
        if date_end < curr_sem.end_date.date():
            date_end = curr_sem.end_date.date()
        index = all_semesters.index(sem)
        if index > 0:
            curr_sem = Semester.objects.get(name=all_semesters[index-1])
            if date_start > curr_sem.end_date.date():
                date_start = curr_sem.end_date.date()
        else:
            date_start = datetime.strptime('15092008', '%d%m%Y').date()
    date_start += timedelta(days=1)

    total = 0.0
    data = []
    for section in sections:
        for sem in semesters:
            dict = {}
            dict['section'] = section
            dict['semester'] = sem
            dict['amount'] = __compute_bill(semester=sem, faculty=faculty, section=section)
            total += dict['amount']
            data.append(dict)

    __create_PDF(
        faculty=faculty,
        date_start=date_start.strftime("%d.%m.%y"),
        date_end=date_end.strftime("%d.%m.%y"),
        data=data,
        total=total
    )

    return render(
        request,
        'bill2myprint/bill.html',
        {
            'all_semesters': all_semesters,
            'semesters': semesters,
            'faculty': faculty,
            'date_start': date_start,
            'date_end': date_end,
            'data': data,
            'total': total,
            'semesters_length': str(len(semesters))
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
