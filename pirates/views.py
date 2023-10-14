from django.shortcuts import render
from django.views import View
from .models import Tesouro
from django.db.models import F, ExpressionWrapper, DecimalField, Sum

class ListaTesouros(View):
     def get(self, request):

        type_total_value = DecimalField(max_digits=10, decimal_places=2)
        total_value = ExpressionWrapper(F('preco') * F('quantidade'), output_field=type_total_value)

        tesouros = Tesouro.objects.annotate(valor_total=total_value)

        
        context = {'lista_tesouros': tesouros}
        context.update(tesouros.aggregate(total_geral=Sum('valor_total', output_field=type_total_value)))

        return render(request, 'lista_tesouros.html', context)