from django.shortcuts import render, get_object_or_404
# Authentication imports
from django.contrib.auth.decorators import login_required # for custom views (functions)
from django.contrib.auth.mixins import LoginRequiredMixin # for generic views (classes)

from django.views.generic import ListView
#from django.http import HttpResponseRedirect, HttpResponseNotFound
#from django.urls import reverse

# Custom models
from uniflow.models import ServiceconsumerT, BudgettransactionsT
from bill2myprint.models import *

from django.db.models import Sum


def index(request):
    context = {'text': 'Hello world !'}
    return render(request, 'bill2myprint/index.html', context)

def students(request):
    context = {}
    context['semesters'] =  Semester.objects.values_list('name', flat=True)
    print(request.POST)
    if request.POST:
        semesters_asked = request.POST.getlist('semesters[]')
        if semesters_asked:
            data = []
            for student in Student.objects.all():
                for s_asked in semesters_asked:
                    vpsi = 24
                    fac = student.transaction_set.filter(semester__name=s_asked, transaction_type='FACULTY_ALLOWANCE').annotate(total=Sum('amount'))[0].total
                    added = student.transaction_set.filter(semester__name=s_asked, transaction_type='ACCOUNT_CHARGING').annotate(total=Sum('amount'))[0].total
                    spent = student.transaction_set.filter(Q(transaction__transaction_type='PRINT_JOB')|Q(transaction__transaction_type='REFUND'), semester__name=s_asked).annotate(total=Sum('amount'))[0].total
                    data.append({
                        'sciper': student.sciper,
                        'semester': s_asked,
                        'vpsi': vpsi,
                        'fac': fac,
                        'perso': added,
                        'spent': spent
                    })
            context['students': data]
    return render(request, 'bill2myprint/students.html', context)



class SectionsView(LoginRequiredMixin, ListView):
    # Template attributes
    template_name = 'bill2myprint/sections.html'
    context_object_name = 'section_list'

    def get_queryset(self):
        # The "S_StudU" part is prevented from being displayed with to the "cut" templatetag
        return ServiceconsumerT.objects.filter(name__endswith='S_StudU')


class RallongeFacultaireView(LoginRequiredMixin, ListView):
    template_name = 'bill2myprint/rallonge_facultaire.html'
    context_object_name = 'rallonge_list'
    paginate_by = 20

    def get_queryset(self):
        # Get the rallonge facultaire in the BudgetTransaction table
        return BudgettransactionsT.objects.filter(transactiondata__startswith='Rallonge')


class RallongeFacultaire2View(LoginRequiredMixin, ListView):
    template_name = 'bill2myprint/rallonge_facultaire.html'
    context_object_name = 'rallonge2_list'

    def get_queryset(self):
        # Get the rallonge facultaire in the BudgetTransaction table
        return BudgettransactionsT.objects.filter(transactiondata__startswith='Rallonge').values('amount', 'transactiondata').distinct()


class StudentsView(LoginRequiredMixin, ListView):
    template_name = 'bill2myprint/etudiants.html'
    context_object_name = 'students_list'
    paginate_by = 15

    def get_queryset(self):
        # Get the students list
        students_group_id = ServiceconsumerT.objects.get(name='Etudiant').id
        students_cost_center_id = ServiceconsumerT.objects.get(name='ETU').id
        return ServiceconsumerT.objects.filter(defaultgroupid=students_group_id, defaultcostcenter=students_cost_center_id)


class StudentDetailView(LoginRequiredMixin, ListView):
    template_name = 'bill2myprint/etudiant_detail.html'
    context_object_name = 'transactions_list'
    paginate_by = 15

    def get_queryset(self):
        # Get the student's transaction history
        student_id = self.kwargs['studid']
        return ServiceconsumerT.objects.get(pk=student_id).budgettransactionst_set.all()


@login_required
def studentTotal(request, studid):
    # Output total of student depense
    template_name = 'bill2myprint/etudiant_total.html'
    student = ServiceconsumerT.objects.get(pk=studid)
    total = student.budgettransactionst_set.aggregate(Sum('amount'))['amount__sum']
    name = student.name
    return render(request, template_name, {'total': total, 'name': name})
