from django.shortcuts import render
from django.db.models import F,ExpressionWrapper,DecimalField
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from django.contrib.auth.models import User
from . import models

class SalvarTesouro():
    model = models.Tesouro
    fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
    template_name = 'salvar_tesouro.html'
    success_url = reverse_lazy('lista_tesouros')

class InserirTesouro(LoginRequiredMixin, SalvarTesouro, CreateView):

    def form_valid(self, form):
        tesouro = form.save(commit=False)
        tesouro.user = self.request.user
        tesouro.save()
        return super(SalvarTesouro, self).form_valid(form)

class AtualizarTesouro(LoginRequiredMixin, SalvarTesouro, UpdateView):
    pass

class RemoverTesouro(LoginRequiredMixin, DeleteView):
    model = models.Tesouro
    success_url = reverse_lazy('lista_tesouros')
    template_name = 'clipping_confirm_delete.html'

class ListarTesouros(LoginRequiredMixin, ListView):
    model = models.Tesouro
    template_name = 'lista_tesouros.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_geral'] = 0
        for obj in context['object_list']:
            context['total_geral'] += obj.valor_total
        return context

    def get_queryset(self, **kwargs):
        queryset = models.Tesouro.objects.annotate(valor_total=ExpressionWrapper(F('quantidade')*F('preco'),\
                            output_field=DecimalField(max_digits=10,\
                                                    decimal_places=2,\
                                                     blank=True)\
                                                    )\
                            )
        return queryset.filter(user=self.request.user)