from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.db import models

from .models import Intrant, MouvementStock
from .forms import IntrantForm, MouvementStockForm


class IntrantListView(LoginRequiredMixin, ListView):
    model = Intrant
    template_name = 'stock/liste_intrants.html'
    context_object_name = 'intrants'
    paginate_by = 20

    def get_queryset(self):
        queryset = Intrant.objects.all()
        recherche = self.request.GET.get('q')
        if recherche:
            queryset = queryset.filter(models.Q(nom__icontains=recherche) | models.Q(description__icontains=recherche))
        return queryset.order_by('nom')


class IntrantCreateView(LoginRequiredMixin, CreateView):
    model = Intrant
    form_class = IntrantForm
    template_name = 'stock/ajouter_intrant.html'
    success_url = reverse_lazy('stock:liste_intrants')

    def form_valid(self, form):
        messages.success(self.request, f'Intrant "{form.instance.nom}" créé avec succès.')
        return super().form_valid(form)


class IntrantUpdateView(LoginRequiredMixin, UpdateView):
    model = Intrant
    form_class = IntrantForm
    template_name = 'stock/ajouter_intrant.html'
    success_url = reverse_lazy('stock:liste_intrants')

    def form_valid(self, form):
        messages.success(self.request, f'Intrant "{form.instance.nom}" modifié avec succès.')
        return super().form_valid(form)


class MouvementStockListView(LoginRequiredMixin, ListView):
    model = MouvementStock
    template_name = 'stock/mouvements.html'
    context_object_name = 'mouvements'
    paginate_by = 20

    def get_queryset(self):
        return MouvementStock.objects.select_related('intrant', 'responsable').order_by('-date_mouvement')


class MouvementStockCreateView(LoginRequiredMixin, CreateView):
    model = MouvementStock
    form_class = MouvementStockForm
    template_name = 'stock/entree_stock.html'
    success_url = reverse_lazy('stock:mouvements')

    def form_valid(self, form):
        mouvement = form.save(commit=False)
        if mouvement.type_mouvement == 'entree':
            mouvement.intrant.quantite += mouvement.quantite
        else:
            mouvement.intrant.quantite -= mouvement.quantite
        mouvement.intrant.save()
        mouvement.save()
        messages.success(self.request, f'Mouvement de stock enregistré avec succès.')
        return super().form_valid(form)


class MouvementStockDetailView(LoginRequiredMixin, DetailView):
    model = MouvementStock
    template_name = 'stock/mouvements.html'
    context_object_name = 'mouvement'


class AlerteStockView(LoginRequiredMixin, ListView):
    model = Intrant
    template_name = 'stock/alertes.html'
    context_object_name = 'intrants'

    def get_queryset(self):
        return Intrant.objects.filter(seuil_alerte__isnull=False).order_by('quantite')
