from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db import models
from django.forms import inlineformset_factory
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from .models import Client, VENTE, VenteArticle
from .forms import ClientForm, VenteForm, VenteArticleForm

User = get_user_model()

VenteArticleFormSet = inlineformset_factory(
    VENTE,
    VenteArticle,
    form=VenteArticleForm,
    fields=('culture', 'parcelle', 'quantite', 'prix_unitaire'),
    extra=1,
    can_delete=True,
)


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
        return queryset.order_by('-date_commande', '-date_creation', '-pk')


class VenteDetailView(LoginRequiredMixin, DetailView):
    model = VENTE
    template_name = 'ventes/detail.html'
    context_object_name = 'vente'


class VenteCreateView(LoginRequiredMixin, CreateView):
    model = VENTE
    form_class = VenteForm
    template_name = 'ventes/vente_form.html'
    success_url = reverse_lazy('ventes:liste')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_formset'] = kwargs.get(
            'article_formset', VenteArticleFormSet(instance=VENTE())
        )
        return context

    def form_valid(self, form):
        article_formset = VenteArticleFormSet(self.request.POST, instance=VENTE())
        if not article_formset.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, article_formset=article_formset)
            )
        self.object = form.save()
        article_formset.instance = self.object
        article_formset.save()
        self.object.recalculer_total()
        messages.success(self.request, 'Vente enregistrée avec succès.')
        return redirect(self.get_success_url())


class VenteUpdateView(LoginRequiredMixin, UpdateView):
    model = VENTE
    form_class = VenteForm
    template_name = 'ventes/vente_form.html'
    success_url = reverse_lazy('ventes:liste')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_formset'] = kwargs.get(
            'article_formset', VenteArticleFormSet(instance=self.object)
        )
        return context

    def form_valid(self, form):
        article_formset = VenteArticleFormSet(self.request.POST, instance=self.object)
        if not article_formset.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, article_formset=article_formset)
            )
        self.object = form.save()
        article_formset.instance = self.object
        article_formset.save()
        self.object.recalculer_total()
        messages.success(self.request, 'Vente mise à jour avec succès.')
        return redirect(self.get_success_url())


class FactureDetailView(LoginRequiredMixin, DetailView):
    model = VENTE
    template_name = 'ventes/facture.html'
    context_object_name = 'vente'


class VentePDFView(LoginRequiredMixin, View):
    def get(self, request, pk):
        vente = VENTE.objects.select_related('client').prefetch_related('articles').get(pk=pk)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="facture-vente-{vente.pk}.pdf"'

        document = SimpleDocTemplate(
            response,
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm,
        )
        styles = getSampleStyleSheet()
        elements = [
            Paragraph('SmartFarm', styles['Title']),
            Paragraph(f'FACTURE DE VENTE - FAC-{vente.pk}', styles['Heading2']),
            Paragraph(f'Date : {vente.date_commande:%d/%m/%Y}', styles['Normal']),
            Paragraph(f'Client : {vente.client or "Client non renseigné"}', styles['Normal']),
            Spacer(1, 10 * mm),
        ]

        rows = [['Description', 'Quantité', 'Prix unitaire', 'Total']]
        for article in vente.articles.all():
            rows.append([
                str(article.culture or article.parcelle or 'Article'),
                str(article.quantite),
                f'{article.prix_unitaire:.2f} FCFA',
                f'{article.montant_total():.2f} FCFA',
            ])
        if len(rows) == 1:
            rows.append(['Aucun article', '', '', ''])
        rows.append(['', '', 'Total', f'{vente.total:.2f} FCFA'])

        table = Table(rows, colWidths=[75 * mm, 25 * mm, 35 * mm, 35 * mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d7d3a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (-2, -1), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f1f8f2')),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ]))
        elements.append(table)
        document.build(elements)
        return response


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
    success_url = reverse_lazy('ventes:clients_liste')

    def form_valid(self, form):
        messages.success(self.request, 'Client ajouté avec succès.')
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/modifier.html'
    success_url = reverse_lazy('ventes:clients_liste')

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
    success_url = reverse_lazy('ventes:commandes_liste')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_formset'] = kwargs.get(
            'article_formset', VenteArticleFormSet(instance=VENTE())
        )
        return context

    def form_valid(self, form):
        article_formset = VenteArticleFormSet(self.request.POST, instance=VENTE())
        if not article_formset.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, article_formset=article_formset)
            )
        self.object = form.save()
        article_formset.instance = self.object
        article_formset.save()
        self.object.recalculer_total()
        messages.success(self.request, 'Commande enregistrée avec succès.')
        return redirect(self.get_success_url())


class CommandeUpdateView(LoginRequiredMixin, UpdateView):
    model = VENTE
    form_class = VenteForm
    template_name = 'commandes/ajouter.html'
    success_url = reverse_lazy('ventes:commandes_liste')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_formset'] = kwargs.get(
            'article_formset', VenteArticleFormSet(instance=self.object)
        )
        return context

    def form_valid(self, form):
        article_formset = VenteArticleFormSet(self.request.POST, instance=self.object)
        if not article_formset.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, article_formset=article_formset)
            )
        self.object = form.save()
        article_formset.instance = self.object
        article_formset.save()
        self.object.recalculer_total()
        messages.success(self.request, 'Commande mise à jour avec succès.')
        return redirect(self.get_success_url())


class CommandeFactureView(LoginRequiredMixin, DetailView):
    model = VENTE
    template_name = 'commandes/facture.html'
    context_object_name = 'commande'
