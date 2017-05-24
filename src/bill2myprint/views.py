import time
from django.shortcuts import render
# Authentication imports
from django.contrib.auth.decorators import login_required # for custom views (functions)
from django.contrib.auth.mixins import LoginRequiredMixin # for generic views (classes)

from django.views.generic import ListView

# Custom models
from uniflow.models import ServiceconsumerT, BudgettransactionsT
from bill2myprint.models import *

from django.db.models import Sum
from django.core.cache import cache


def index(request):
    context = {}
    return render(request, 'bill2myprint/index.html', context)

def students(request):
    context = {}
    context['semesters'] =  Semester.objects.values_list('name', flat=True)

    if request.POST:
        # Get all the semesters selected as objects
        semesters_asked = request.POST.getlist('semesters[]')
        semesters_objects = [Semester.objects.get(name=s) for s in semesters_asked]

        if semesters_asked:
            # Get all SemesterSummary entries with the corresponding semesters
            data = Semester.objects.none()
            data = SemesterSummary.objects.filter(semester__in=semesters_objects)
            data = data.values('student__sciper',
                               'semester__name',
                               'myprint_allowance',
                               'faculty_allowance',
                               'total_charged',
                               'total_spent')
            context['students'] = data
    return render(request, 'bill2myprint/students.html', context)

def faculties(request):
    context = {}
    context['semesters'] =  Semester.objects.values_list('name', flat=True)
    if request.POST:
        # Get all the semesters selected as objects
        semester_asked = request.POST.getlist('semesters[]')
        semesters_objects = [Semester.objects.get(name=s) for s in semester_asked]

        if semester_asked:
            # Get all SemesterSummary entries with the corresponding semesters
            data = Semester.objects.none()
            data = SemesterSummary.objects.filter(semester__in=semesters_objects)
            data = data.values('section__faculty__name', 'semester__name')

            # Aggregate by summing
            data = data.annotate(vpsi=Sum('myprint_allowance'),
                                 fac=Sum('faculty_allowance'),
                                 perso=Sum('total_charged'),
                                 conso=Sum('total_spent')
                                 )
            context['faculties'] = data
    return render(request, 'bill2myprint/faculties.html', context)

def detail(request):
    context = {}
    context['semesters'] = Semester.objects.values_list('name', flat=True)
    context['faculties'] = Faculty.objects.values_list('name', flat=True)
    if request.POST:
        # Get all the semesters selected as objects
        semester_asked = request.POST.getlist('semesters[]')
        semester_objects = [Semester.objects.get(name=s) for s in semester_asked]

        # Get the faculty selected as object
        faculty_objects = Faculty.objects.get(name=request.POST.get('faculties[]'))

        # Get all sections from that faculty
        section_objects = faculty_objects.section_set.all()

        if semester_asked and faculty_objects:
            # Get all SemesterSummary entries with the corresponding section and semester
            data = Semester.objects.none()
            data = SemesterSummary.objects.filter(section__in=section_objects, semester__in=semester_objects)
            data = data.values('student__sciper', 
                    'section__acronym', 
                    'semester__name',
                    'myprint_allowance',
                    'faculty_allowance',
                    'total_spent')

            def compute_fac_cost(student):
                """
                Function computing the amount the faculty will be billed
                for the given student.
                It adds the key,value pair: 'faculty_cost' -> amount
                """
                vpsi = student['myprint_allowance']
                fac = student['faculty_allowance']
                spent = round(student['total_spent'], 2)
                student['total_spent'] = spent # update to rounded value
                
                fac_cost = 0.0
                diff_vpsi = spent + vpsi
                if diff_vpsi < 0:       # used all of vpsi credit
                    if abs(diff_vpsi) < fac: # used part of fac credit only
                        fac_cost = -round(diff_vpsi, 2)
                    else:
                        fac_cost = round(fac, 2)  # used all of fac credit
                student['faculty_cost'] = fac_cost
                return student

            student_data = []
            section_data = {}
            
            for student in data:
                # Add the faculty_cost field to each student
                student_data.append(compute_fac_cost(student))

                # Aggregate the faculty_cost by section
                section = student['section__acronym']
                if section in section_data:
                    section_data[section]['faculty_cost'] += student['faculty_cost']
                else:
                    section_data[section] = {
                            'section__acronym': section,
                            'faculty_cost': student['faculty_cost']
                            }

            # Round all values of faculty costs
            for section in section_data.values():
                section['faculty_cost'] = round(section['faculty_cost'], 2)

            context['sections'] = section_data.values()

            # Send detail by student only if asked
            if request.POST.get('student', False):
                context['students'] = student_data

    return render(request, 'bill2myprint/detail.html', context)
        

class RallongeFacultaire2View(LoginRequiredMixin, ListView):
    template_name = 'bill2myprint/rallonge_facultaire.html'
    context_object_name = 'rallonge2_list'

    def get_queryset(self):
        # Get the rallonge facultaire in the BudgetTransaction table
        return BudgettransactionsT.objects.filter(transactiondata__startswith='Rallonge').values('amount', 'transactiondata').distinct()
