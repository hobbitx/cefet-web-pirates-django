from django.shortcuts import render
from django.views import View
from .models import Tesouro
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .forms import *

class ListaTesouros(View):
     def get(self, request):
        tesouros = Tesouro.objects.all()
        valor_total = 0
        for tesouro in tesouros:
           valor_total = valor_total + tesouro.valor_total

        return render(request, 'lista_tesouros.html', {'lista_tesouros': tesouros, 'total': valor_total})



class SalvarTesouro(View):
    def get(self, request, id=None):
        try:
            tesouro = Tesouro.objects.get(id=id)
        except Tesouro.DoesNotExist:
            tesouro = None

        return render(request, 'salvar_tesouro.html', {'form': SalvarTesouroForm(instance=tesouro)})

    def post(self, request, id=None):
        try:
            tesouro = Tesouro.objects.get(id=id)
        except Tesouro.DoesNotExist:
            tesouro = None

        form = SalvarTesouroForm(request.POST, request.FILES, instance=tesouro)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ListaTesouros'))

        return render(request, 'salvar_tesouro.html', {'form': form})


class ExcluirTesouro(View):
    def get(self, request, id):
        try:
            tesouro = Tesouro.objects.get(id=id)
            tesouro.delete()
        except Tesouro.DoesNotExist:
            return HttpResponseNotFound()
        return HttpResponseRedirect(reverse('ListaTesouros'))
        