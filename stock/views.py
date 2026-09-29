from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.db import models, transaction
from django.db.models import DecimalField, ExpressionWrapper, F
from django.core.exceptions import ValidationError

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
        with transaction.atomic():
            intrant = Intrant.objects.select_for_update().get(pk=form.cleaned_data['intrant'].pk)
            mouvement = form.save(commit=False)
            mouvement.intrant = intrant
            if mouvement.type_mouvement == 'entree':
                intrant.quantite += mouvement.quantite
            elif mouvement.quantite > intrant.quantite:
                form.add_error(
                    'quantite',
                    ValidationError('La quantité sortie ne peut pas dépasser le stock disponible.'),
                )
                return self.form_invalid(form)
            else:
                intrant.quantite -= mouvement.quantite
            intrant.save(update_fields=['quantite', 'date_modification'])
            mouvement.save()
            self.object = mouvement
        messages.success(self.request, f'Mouvement de stock enregistré avec succès.')
        return redirect(self.get_success_url())


class MouvementStockDetailView(LoginRequiredMixin, DetailView):
    model = MouvementStock
    template_name = 'stock/mouvement_detail.html'
    context_object_name = 'mouvement'


class AlerteStockView(LoginRequiredMixin, ListView):
    model = Intrant
    template_name = 'stock/alertes.html'
    context_object_name = 'intrants'

    def get_queryset(self):
        return Intrant.objects.filter(
            seuil_alerte__isnull=False,
            quantite__lte=F('seuil_alerte'),
        ).annotate(
            ecart=ExpressionWrapper(
                F('seuil_alerte') - F('quantite'),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        ).order_by('quantite')
