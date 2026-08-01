from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db import models

from .models import Client, VENTE, VenteArticle
from .forms import ClientForm, VenteForm, VenteArticleForm

User = get_user_model()


class VenteListView(LoginRequiredMixin, ListView):
    model = VENTE
    template_name = 'ventes/liste.html'
    context_object_name = 'ventes'
    paginate_by = 20

    def get_queryset(self):
        queryset = VENTE.objects.select_related('client', 'responsable').all()
        recherche = self.request.GET.get('q')
        statut = self.request.GET.get('statut')

        if statut:
            queryset = queryset.filter(statut=statut)
        if recherche:
            queryset = queryset.filter(
                models.Q(client__nom__icontains=recherche)
                | models.Q(description__icontains=recherche)
            )
        return queryset.order_by('-date_commande')


class VenteDetailView(LoginRequiredMixin, DetailView):
    model = VENTE
    template_name = 'ventes/detail.html'
    context_object_name = 'vente'


class VenteCreateView(LoginRequiredMixin, CreateView):
    model = VENTE
    form_class = VenteForm
    template_name = 'ventes/vente_form.html'
    success_url = reverse_lazy('ventes:liste')

    def form_valid(self, form):
        messages.success(self.request, 'Vente enregistrée avec succès.')
        return super().form_valid(form)


class VenteUpdateView(LoginRequiredMixin, UpdateView):
    model = VENTE
    form_class = VenteForm
    template_name = 'ventes/vente_form.html'
    success_url = reverse_lazy('ventes:liste')

    def form_valid(self, form):
        messages.success(self.request, 'Vente mise à jour avec succès.')
        return super().form_valid(form)


class FactureDetailView(LoginRequiredMixin, DetailView):
    model = VENTE
    template_name = 'ventes/facture.html'
    context_object_name = 'vente'


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/liste.html'
    context_object_name = 'clients'
    paginate_by = 20

    def get_queryset(self):
        queryset = Client.objects.all()
        recherche = self.request.GET.get('q')

        if recherche:
            queryset = queryset.filter(
                models.Q(nom__icontains=recherche)
                | models.Q(email__icontains=recherche)
                | models.Q(ville__icontains=recherche)
            )

        return queryset.order_by('nom')


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'clients/detail.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commandes_recents'] = self.object.ventes.order_by('-date_commande')[:5]
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/ajouter.html'
    success_url = reverse_lazy('clients:liste')

    def form_valid(self, form):
        messages.success(self.request, 'Client ajouté avec succès.')
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/modifier.html'
    success_url = reverse_lazy('clients:liste')

    def form_valid(self, form):
        messages.success(self.request, 'Client mis à jour avec succès.')
        return super().form_valid(form)


class CommandeListView(LoginRequiredMixin, ListView):
    model = VENTE
    template_name = 'commandes/liste.html'
    context_object_name = 'commandes'
    paginate_by = 20

    def get_queryset(self):
        queryset = VENTE.objects.select_related('client', 'responsable').all()
        recherche = self.request.GET.get('q')
        statut = self.request.GET.get('statut')

        if statut:
            queryset = queryset.filter(statut=statut)
        if recherche:
            queryset = queryset.filter(
                models.Q(client__nom__icontains=recherche)
                | models.Q(description__icontains=recherche)
            )

        return queryset.order_by('-date_commande')


class CommandeDetailView(LoginRequiredMixin, DetailView):
    model = VENTE
    template_name = 'commandes/detail.html'
    context_object_name = 'commande'


class CommandeCreateView(LoginRequiredMixin, CreateView):
    model = VENTE
    form_class = VenteForm
    template_name = 'commandes/ajouter.html'
    success_url = reverse_lazy('commandes:liste')

    def form_valid(self, form):
        messages.success(self.request, 'Commande enregistrée avec succès.')
        return super().form_valid(form)


class CommandeUpdateView(LoginRequiredMixin, UpdateView):
    model = VENTE
    form_class = VenteForm
    template_name = 'commandes/ajouter.html'
    success_url = reverse_lazy('commandes:liste')

    def form_valid(self, form):
        messages.success(self.request, 'Commande mise à jour avec succès.')
        return super().form_valid(form)


class CommandeFactureView(LoginRequiredMixin, DetailView):
    model = VENTE
    template_name = 'commandes/facture.html'
    context_object_name = 'commande'
