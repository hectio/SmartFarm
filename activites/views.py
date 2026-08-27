from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db import models

from .models import Activite
from .forms import ActiviteForm


class ActiviteListView(LoginRequiredMixin, ListView):
    model = Activite
    template_name = 'activites/liste.html'
    context_object_name = 'activites'
    paginate_by = 20

    def get_queryset(self):
        queryset = Activite.objects.select_related('parcelle', 'culture', 'responsable').all()
        recherche = self.request.GET.get('q')
        type_activite = self.request.GET.get('type_activite')
        statut = self.request.GET.get('statut')
        parcelle = self.request.GET.get('parcelle')

        if recherche:
            queryset = queryset.filter(
                models.Q(titre__icontains=recherche)
                | models.Q(description__icontains=recherche)
                | models.Q(parcelle__nom__icontains=recherche)
                | models.Q(culture__nom__icontains=recherche)
            )

        if type_activite:
            queryset = queryset.filter(type_activite=type_activite)

        if statut:
            queryset = queryset.filter(statut=statut)

        if parcelle:
            queryset = queryset.filter(parcelle__id=parcelle)

        return queryset.order_by('-date_debut')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from parcelles.models import Parcelle

        context['statuts'] = Activite.STATUT_CHOICES
        context['types'] = Activite.TYPE_CHOICES
        context['parcelles'] = Parcelle.objects.all()
        return context


class ActiviteDetailView(LoginRequiredMixin, DetailView):
    model = Activite
    template_name = 'activites/detail.html'
    context_object_name = 'activite'


class ActiviteCreateView(LoginRequiredMixin, CreateView):
    model = Activite
    form_class = ActiviteForm
    template_name = 'activites/ajouter.html'
    success_url = reverse_lazy('activites:liste')

    def form_valid(self, form):
        messages.success(self.request, f'Activité "{form.instance.titre}" créée avec succès.')
        return super().form_valid(form)


class ActiviteUpdateView(LoginRequiredMixin, UpdateView):
    model = Activite
    form_class = ActiviteForm
    template_name = 'activites/modifier.html'
    success_url = reverse_lazy('activites:liste')

    def form_valid(self, form):
        messages.success(self.request, f'Activité "{form.instance.titre}" modifiée avec succès.')
        return super().form_valid(form)


@login_required
def calendrier(request):
    activites = Activite.objects.select_related('parcelle', 'culture').order_by('date_debut')
    return render(request, 'activites/calendrier.html', {'activites': activites})
