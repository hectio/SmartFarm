from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import models

from .models import Culture
from .forms import CultureForm


class CultureListView(LoginRequiredMixin, ListView):
    model = Culture
    template_name = 'cultures/liste.html'
    context_object_name = 'cultures'
    paginate_by = 20

    def get_queryset(self):
        queryset = Culture.objects.select_related('parcelle').all()
        parcelle_id = self.request.GET.get('parcelle')
        statut = self.request.GET.get('statut')
        recherche = self.request.GET.get('q')

        if parcelle_id:
            queryset = queryset.filter(parcelle__id=parcelle_id)
        if statut:
            queryset = queryset.filter(statut=statut)
        if recherche:
            queryset = queryset.filter(
                models.Q(nom__icontains=recherche)
                | models.Q(variete__icontains=recherche)
                | models.Q(parcelle__nom__icontains=recherche)
            )

        return queryset.order_by('-date_semis')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from parcelles.models import Parcelle

        context['parcelles'] = Parcelle.objects.all()
        context['statuts'] = Culture.STATUT_CHOICES
        return context


class CultureDetailView(LoginRequiredMixin, DetailView):
    model = Culture
    template_name = 'cultures/detail.html'
    context_object_name = 'culture'


class CultureCreateView(LoginRequiredMixin, CreateView):
    model = Culture
    form_class = CultureForm
    template_name = 'cultures/ajouter.html'
    success_url = reverse_lazy('cultures:liste')

    def form_valid(self, form):
        messages.success(self.request, f'Culture "{form.instance.nom}" créée avec succès.')
        return super().form_valid(form)


class CultureUpdateView(LoginRequiredMixin, UpdateView):
    model = Culture
    form_class = CultureForm
    template_name = 'cultures/modifier.html'
    success_url = reverse_lazy('cultures:liste')

    def form_valid(self, form):
        messages.success(self.request, f'Culture "{form.instance.nom}" modifiée avec succès.')
        return super().form_valid(form)


class CultureDeleteView(LoginRequiredMixin, DeleteView):
    model = Culture
    template_name = 'cultures/supprimer.html'
    success_url = reverse_lazy('cultures:liste')
    context_object_name = 'culture'

    def delete(self, request, *args, **kwargs):
        culture = self.get_object()
        nom = str(culture)
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Culture "{nom}" supprimée avec succès.')
        return response


@login_required
def calendrier(request):
    cultures = Culture.objects.select_related('parcelle').order_by('date_semis')
    return render(request, 'cultures/calendrier.html', {'cultures': cultures})
