from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from uniflow.models import ServiceconsumerT, BudgettransactionsT
from bill2myprint.models import *
from django.db.models import Sum, Q

import json


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
        annotate(amount=Sum('total_spent'))

    number_of_students = __get_number_of_students(semester=current_semester)

    return render(
        request,
        'bill2myprint/homepage.html',
        {
            'is_homepage': True,
            'current_semester': current_semester,
            'semesters': semesters,
            'faculties': faculties,
            'last_update': "18 mai 2017 08:25",
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
        dict = {}
        dict['section'] = section
        if section_data:
            dict['vpsi'] = section_data.aggregate(credit=Sum('myprint_allowance'))['credit']
            dict['faculty'] = section_data.aggregate(credit=Sum('faculty_allowance'))['credit']
            dict['add_students'] = section_data.aggregate(credit=Sum('total_charged'))['credit']
            dict['students'] = section_data.aggregate(credit=Sum('total_spent'))['credit']
            dict['amount'] = 0
        else:
            dict['vpsi'] = 0
            dict['faculty'] = 0
            dict['add_students'] = 0
            dict['students'] = 0
            dict['amount'] = 0
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

    current_section = section if section else \
        request.POST['section'] if 'section' in request.POST and request.POST['section'] in sections else sections[0]

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
            'students': students,
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

        credit = transactions.aggregate(credit=Sum('amount'))['credit']
        transactions = transactions.order_by("-transaction_date")

    elif student_name:
        try:
            student = Student.objects.get(name=student_name)
        except ObjectDoesNotExist:
            student = None

        transactions = Transaction.objects.filter(student__name=student_name)

        credit = transactions.aggregate(credit=Sum('amount'))['credit']
        transactions = transactions.order_by("-transaction_date")

    else:
        student = None
        transactions = None
        credit = 0

    return render(
        request,
        'bill2myprint/students.html',
        {
            'is_students': True,
            'student': student,
            'transactions': transactions,
            'credit': credit,
        }
    )


    """
    data = ()
    if request.POST:
        semesters_asked = request.POST.getlist('semesters[]')
        semesters_objects = [Semester.objects.get(name=s) for s in semesters_asked]
        if semesters_asked:
            data = Semester.objects.none()
            data = SemesterSummary.objects.filter(semester__in=semesters_objects)
            data = data.values('student__sciper',
                               'semester__name',
                               'myprint_allowance',
                               'faculty_allowance',
                               'total_charged',
                               'total_spent')

    return render(
        request,
        'bill2myprint/students.html',
        {
            'is_students': True,
            'semesters':  Semester.objects.values_list('name', flat=True),
            'students': data,
        }
    )
    """


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
    return render(
        request,
        'bill2myprint/status.html',
        {
            'is_miscellaneous': True,
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


#class SectionsView(LoginRequiredMixin, ListView):
#    # Template attributes
#    template_name = 'bill2myprint/sections.html'
#    context_object_name = 'section_list'
#
#    def get_queryset(self):
#        # The "S_StudU" part is prevented from being displayed with to the "cut" templatetag
#        return ServiceconsumerT.objects.filter(name__endswith='S_StudU')


#class RallongeFacultaireView(LoginRequiredMixin, ListView):
#    template_name = 'bill2myprint/rallonge_facultaire.html'
#    context_object_name = 'rallonge_list'
#    paginate_by = 20
#
#    def get_queryset(self):
#        # Get the rallonge facultaire in the BudgetTransaction table
#        return BudgettransactionsT.objects.filter(transactiondata__startswith='Rallonge')


class RallongeFacultaire2View(LoginRequiredMixin, ListView):
    template_name = 'bill2myprint/rallonge_facultaire.html'
    context_object_name = 'rallonge2_list'

    def get_queryset(self):
        # Get the rallonge facultaire in the BudgetTransaction table
        return BudgettransactionsT.objects.filter(transactiondata__startswith='Rallonge').values('amount', 'transactiondata').distinct()


#class StudentsView(LoginRequiredMixin, ListView):
#    template_name = 'bill2myprint/etudiants.html'
#    context_object_name = 'students_list'
#    paginate_by = 15
#
#    def get_queryset(self):
#        # Get the students list
#        students_group_id = ServiceconsumerT.objects.get(name='Etudiant').id
#        students_cost_center_id = ServiceconsumerT.objects.get(name='ETU').id
#        return ServiceconsumerT.objects.filter(defaultgroupid=students_group_id, defaultcostcenter=students_cost_center_id)


#class StudentDetailView(LoginRequiredMixin, ListView):
#    template_name = 'bill2myprint/etudiant_detail.html'
#    context_object_name = 'transactions_list'
#    paginate_by = 15
#
#    def get_queryset(self):
#        # Get the student's transaction history
#        student_id = self.kwargs['studid']
#        return ServiceconsumerT.objects.get(pk=student_id).budgettransactionst_set.all()
#
#
#@login_required
#def studentTotal(request, studid):
#    # Output total of student depense
#    template_name = 'bill2myprint/etudiant_total.html'
#    student = ServiceconsumerT.objects.get(pk=studid)
#    total = student.budgettransactionst_set.aggregate(Sum('amount'))['amount__sum']
#    name = student.name
#    return render(request, template_name, {'total': total, 'name': name})
