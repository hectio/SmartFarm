from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.db import models
from django.db.models import Q

from .models import Parcelle
from .forms import ParcelleForm


class ParcelleListView(LoginRequiredMixin, ListView):
    """
    Vue pour afficher la liste de toutes les parcelles.
    """
    model = Parcelle
    template_name = 'parcelles/liste.html'
    context_object_name = 'parcelles'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Parcelle.objects.all()
        
        # Filtres optionnels
        statut = self.request.GET.get('statut')
        exploitation = self.request.GET.get('exploitation')
        recherche = self.request.GET.get('q')
        
        if statut:
            queryset = queryset.filter(statut=statut)
        
        if exploitation:
            queryset = queryset.filter(exploitation__id=exploitation)
        
        if recherche:
            queryset = queryset.filter(
                Q(nom__icontains=recherche) | Q(code__icontains=recherche)
            )
        
        return queryset.order_by('-date_creation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from exploitation.models import Exploitation
        context['exploitations'] = Exploitation.objects.all()
        context['statuts'] = Parcelle.STATUT_CHOICES
        return context


class ParcelleDetailView(LoginRequiredMixin, DetailView):
    """
    Vue pour afficher les détails d'une parcelle spécifique.
    """
    model = Parcelle
    template_name = 'parcelles/detail.html'
    context_object_name = 'parcelle'


class ParcelleCreateView(LoginRequiredMixin, CreateView):
    """
    Vue pour créer une nouvelle parcelle.
    """
    model = Parcelle
    form_class = ParcelleForm
    template_name = 'parcelles/ajouter.html'
    success_url = reverse_lazy('parcelles:parcelle_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'La parcelle "{form.instance.nom}" a été créée avec succès.')
        return super().form_valid(form)


class ParcelleUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vue pour modifier une parcelle existante.
    """
    model = Parcelle
    form_class = ParcelleForm
    template_name = 'parcelles/modifier.html'
    success_url = reverse_lazy('parcelles:parcelle_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'La parcelle "{form.instance.nom}" a été modifiée avec succès.')
        return super().form_valid(form)


class ParcelleDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vue pour supprimer une parcelle.
    """
    model = Parcelle
    template_name = 'parcelles/supprimer.html'
    success_url = reverse_lazy('parcelles:parcelle_list')
    context_object_name = 'parcelle'
    
    def delete(self, request, *args, **kwargs):
        parcelle = self.get_object()
        nom = parcelle.nom
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'La parcelle "{nom}" a été supprimée avec succès.')
        return response
