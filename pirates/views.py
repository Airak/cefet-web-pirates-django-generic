from django.shortcuts import render
from django.db.models import F,ExpressionWrapper,DecimalField
from django.views import View
from django.urls import reverse_lazy

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from . import models

class SalvarTesouro():
    model = models.Tesouro
    fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
    template_name = 'salvar_tesouro.html'
    success_url = reverse_lazy('lista_tesouros')

class InserirTesouro(SalvarTesouro, CreateView):
    pass

class AtualizarTesouro(SalvarTesouro, UpdateView):
    pass

class RemoverTesouro(DeleteView):
    model = models.Tesouro
    success_url = reverse_lazy('lista_tesouros')
    template_name = 'clipping_confirm_delete.html'

class ListarTesouros(View):
    def get(self,request):
        lst_tesouros = models.Tesouro.objects.annotate(valor_total=ExpressionWrapper(F('quantidade')*F('preco'),\
                            output_field=DecimalField(max_digits=10,\
                                                    decimal_places=2,\
                                                     blank=True)\
                                                    )\
                            )
        valor_total = 0
        for tesouro in lst_tesouros:
            valor_total += tesouro.valor_total
        return render(request,"lista_tesouros.html",{"lista_tesouros":lst_tesouros,
                                                     "total_geral":valor_total})
