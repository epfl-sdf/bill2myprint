from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse

def index(request):
    context = {'text': 'Hello world !'}
    return render(request, 'hello_world/login_out.html', context)


@login_required
def logged(request):
    context = {'text': 'Logged !'}
    return render(request, 'hello_world/login_out.html', context)
