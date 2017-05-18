from django.shortcuts import render, get_object_or_404
# Authentication imports
from django.contrib.auth.decorators import login_required # for custom views (functions)
from django.contrib.auth.mixins import LoginRequiredMixin # for generic views (classes)

from django.views.generic import ListView

# Custom models
from uniflow.models import ServiceconsumerT, BudgettransactionsT
from bill2myprint.models import *

from django.db.models import Sum, Case, When, F, Q, FloatField, Value
from django.core.cache import cache


def index(request):
    context = {'text': 'Hello world !'}
    return render(request, 'bill2myprint/index.html', context)

@login_required
def students(request):
    context = {}
    context['semesters'] =  Semester.objects.values_list('name', flat=True)
    print(request.POST)
    if request.POST:
        semesters_asked = request.POST.getlist('semesters[]')
        semesters_objects = [Semester.objects.get(name=s) for s in semesters_asked]
        if semesters_asked:
            data = Semester.objects.none()
            for s_asked in semesters_objects:
                data = data | s_asked.transaction_set.values('student__sciper', 'semester__name').annotate(
                    vpsi=Value(24.0, FloatField()),
                    fac=Sum(Case(
                        When(transaction_type='FACULTY_ALLOWANCE', then=F('amount')),
                        default=0.0,
                        output_field=FloatField(),
                    )),
                    perso=Sum(Case(
                        When(transaction_type='ACCOUNT_CHARGING', then=F('amount')),
                        default=0.0,
                        output_field=FloatField(),
                    )),
                    spent=Sum(Case(
                        When(Q(transaction_type='PRINT_JOB') | Q(transaction_type='REFUND'), then=F('amount')),
                        default=0.0,
                        output_field=FloatField(),
                    ))
                )
            context['students'] = data
    return render(request, 'bill2myprint/students.html', context)

@login_required
def faculties(request):
    context = {}
    context['semesters'] =  Semester.objects.values_list('name', flat=True)
    if request.POST:
        semester_asked = request.POST.getlist('semesters[]')
        semesters_objects = [Semester.objects.get(name=s) for s in semester_asked]
        if semester_asked:
            data = Semester.objects.none()
            for s_asked in semesters_objects:
                data = data | s_asked.transaction_set.values('section__faculty__name', 'semester__name').annotate(
                            vpsi=Sum(Case(
                            When(transaction_type='MYPRINT_ALLOWANCE', then=F('amount')),
                            default=0.0,
                            output_field=FloatField(),
                        )),
                        fac=Sum(Case(
                            When(transaction_type='FACULTY_ALLOWANCE', then=F('amount')),
                            default=0.0,
                            output_field=FloatField(),
                        )),
                        perso=Sum(Case(
                            When(transaction_type='ACCOUNT_CHARGING', then=F('amount')),
                            default=0.0,
                            output_field=FloatField(),
                        )),
                        conso=Sum(Case(
                            When(Q(transaction_type='PRINT_JOB') | Q(transaction_type='REFUND'), then=F('amount')),
                            default=0.0,
                            output_field=FloatField(),
                        ))
                    )
           #for faculty in Faculty.objects.all():
           #    section_semester_data = Section.objects.none()
           #    for s_asked in semesters_objects:
           #        for sec in faculty.section_set.all():
           #            section_semester_data = section_semester_data | sec.transaction_set.filter(semester=s_asked).values('section__name', 'semester__name').annotate(
           #                    vpsi=Sum(Case(
           #                        When(transaction_type='MYPRINT_ALLOWANCE', then=F('amount')),
           #                        default=0.0,
           #                        output_field=FloatField(),
           #                    )),
           #                    fac=Sum(Case(
           #                        When(transaction_type='FACULTY_ALLOWANCE', then=F('amount')),
           #                        default=0.0,
           #                        output_field=FloatField(),
           #                    )),
           #                    perso=Sum(Case(
           #                        When(transaction_type='ACCOUNT_CHARGING', then=F('amount')),
           #                        default=0.0,
           #                        output_field=FloatField(),
           #                    )),
           #                    conso=Sum(Case(
           #                        When(Q(transaction_type='PRINT_JOB') | Q(transaction_type='REFUND'), then=F('amount')),
           #                        default=0.0,
           #                        output_field=FloatField(),
           #                    ))
           #                )
           #        total_vpsi = 0
           #        total_fac = 0
           #        total_conso = 0
           #        for test in section_semester_data:
           #            total_vpsi += test['vpsi']
           #            total_fac += test['fac']
           #            total_conso += test['conso']
           #        data.append({
           #            'faculty': faculty.name,
           #            'semester': s_asked.name,
           #            'vpsi': total_vpsi,
           #            'fac': total_fac,
           #            'conso': total_conso
           #        })
           #       #    transactions = sec.transaction_set.filter(semester__name=s_asked)
           #       #    vpsi_temp = transactions.filter(transaction_type='MYPRINT_ALLOWANCE').aggregate(total=Sum('amount'))['total']
           #       #    fac_temp = transactions.filter(transaction_type='FACULTY_ALLOWANCE').aggregate(total=Sum('amount'))['total']
           #       #    conso_temp = transactions.filter(Q(transaction_type='PRINT_JOB')|Q(transaction_type='REFUND')).aggregate(total=Sum('amount'))['total']
           #       #    if not vpsi_temp:
           #       #        vpsi_temp = 0
           #       #    if not fac_temp:
           #       #        fac_temp = 0
           #       #    if not conso_temp:
           #       #        conso_temp = 0
           #       #    vpsi += vpsi_temp
           #       #    fac += fac_temp
           #       #    conso += conso_temp
           #       #data.append({
           #       #    'faculty': faculty.name,
           #       #    'semester': s_asked,
           #       #    'vpsi': vpsi,
           #       #    'fac': fac,
           #       #    'conso': conso
           #       #})
            context['faculties'] = data
    return render(request, 'bill2myprint/faculties.html', context)

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
