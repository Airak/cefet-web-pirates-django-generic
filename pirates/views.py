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

class ListarTesouros(ListView):
    model = models.Tesouro
    template_name = 'lista_tesouros.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_geral'] = 0
        for obj in context['object_list']:
            context['total_geral'] += obj.valor_total
        return context

    def get_queryset(self, **kwargs):
        return models.Tesouro.objects.annotate(valor_total=ExpressionWrapper(F('quantidade')*F('preco'),\
                            output_field=DecimalField(max_digits=10,\
                                                    decimal_places=2,\
                                                     blank=True)\
                                                    )\
                            )