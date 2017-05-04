from django.shortcuts import render, get_object_or_404
# Authentication imports
from django.contrib.auth.decorators import login_required # for custom views (functions)
from django.contrib.auth.mixins import LoginRequiredMixin # for generic views (classes)

from django.views.generic import ListView
#from django.http import HttpResponseRedirect, HttpResponseNotFound
#from django.urls import reverse

from .models import ServiceconsumerT

def index(request):
    context = {'text': 'Hello world !'}
    return render(request, 'bill2myprint/index.html', context)

class SectionsView(LoginRequiredMixin, ListView):
    # Template attributes
    template_name = 'bill2myprint/sections.html'
    context_object_name = 'section_list'

    def get_queryset(self):
	# The "S_StudU" part is prevented from beign displayed with to the defined "cut" templatetag
        return ServiceconsumerT.objects.filter(name__endswith='S_StudU')
    
