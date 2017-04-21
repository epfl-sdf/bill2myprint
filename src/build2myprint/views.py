from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse

from .models import Shoe
from .forms import ShoeForm


def index(request):
    context = {'text': 'Hello world !'}
    return render(request, 'hello_world/login_out.html', context)


@login_required
def logged(request):
    context = {'text': 'Logged !'}
    return render(request, 'hello_world/login_out.html', context)


@login_required
def list_shoes(request):
    shoes = Shoe.objects.all()
    context = {'shoes': shoes}
    return render(request, 'hello_world/list_shoes.html', context)


@login_required
def add_shoe(request):
    if request.method == 'POST':
        form = ShoeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('hello_world:list_shoes'))
    else:
        form = ShoeForm()
    return render(request, 'hello_world/add_shoe.html', {'form': form})


@login_required
def edit_shoe(request, pk):
    shoe = get_object_or_404(Shoe, pk=pk)
    if request.method == 'POST':
        form = ShoeForm(request.POST, instance=shoe)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('hello_world:list_shoes'))
    else:
        form = ShoeForm(instance=shoe)
    return render(request, 'hello_world/edit_shoe.html', {'form': form})
