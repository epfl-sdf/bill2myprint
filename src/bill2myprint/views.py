from django.shortcuts import render, get_object_or_404
# Authentication imports
from django.contrib.auth.decorators import login_required # for custom views (functions)
from django.contrib.auth.mixins import LoginRequiredMixin # for generic views (classes)

from django.views.generic import ListView
#from django.http import HttpResponseRedirect, HttpResponseNotFound
#from django.urls import reverse

from .models import ServiceconsumerT, BudgettransactionsT

def index(request):
    context = {'text': 'Hello world !'}
    return render(request, 'bill2myprint/index.html', context)

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
