from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from datetime import date, timedelta

from django.db import models

from .models import Transaction
from .forms import TransactionForm
from ventes.models import Client


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = 'transactions'
    paginate_by = 20
    transaction_type = None
    template_name = 'finances/recettes.html'

    def get_queryset(self):
        queryset = Transaction.objects.select_related('responsable').all()
        if self.transaction_type:
            queryset = queryset.filter(type_transaction=self.transaction_type)

        categorie = self.request.GET.get('categorie')
        recherche = self.request.GET.get('q')

        if categorie:
            queryset = queryset.filter(categorie=categorie)
        if recherche:
            queryset = queryset.filter(
                models.Q(titre__icontains=recherche)
                | models.Q(description__icontains=recherche)
            )
        return queryset.order_by('-date_operation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_recettes'] = self.get_queryset().filter(
            type_transaction='recette'
        ).aggregate(total=models.Sum('montant'))['total'] or 0
        context['clients_count'] = Client.objects.filter(
            ventes__date_commande__isnull=False
        ).distinct().count()
        return context


class RecetteListView(TransactionListView):
    template_name = 'finances/recettes.html'
    transaction_type = 'recette'


class DepenseListView(TransactionListView):
    template_name = 'finances/depenses.html'
    transaction_type = 'depense'


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finances/transaction_form.html'
    success_url = reverse_lazy('finances:recettes')

    def form_valid(self, form):
        messages.success(self.request, 'Transaction enregistrée avec succès.')
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finances/transaction_form.html'
    success_url = reverse_lazy('finances:recettes')

    def form_valid(self, form):
        messages.success(self.request, 'Transaction mise à jour avec succès.')
        return super().form_valid(form)


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'finances/transaction_form.html'
    success_url = reverse_lazy('finances:recettes')


class FinanceBeneficeView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'finances/benefices.html'
    context_object_name = 'transactions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        month_start = today.replace(day=1)
        previous_month_end = month_start - timedelta(days=1)
        previous_month_start = previous_month_end.replace(day=1)

        month_transactions = Transaction.objects.filter(date_operation__gte=month_start, date_operation__lte=today)
        previous_month_transactions = Transaction.objects.filter(date_operation__gte=previous_month_start, date_operation__lte=previous_month_end)

        current_recettes = month_transactions.filter(type_transaction='recette').aggregate(total=models.Sum('montant'))['total'] or 0
        current_depenses = month_transactions.filter(type_transaction='depense').aggregate(total=models.Sum('montant'))['total'] or 0
        current_benefice = current_recettes - current_depenses
        previous_recettes = previous_month_transactions.filter(type_transaction='recette').aggregate(total=models.Sum('montant'))['total'] or 0
        previous_depenses = previous_month_transactions.filter(type_transaction='depense').aggregate(total=models.Sum('montant'))['total'] or 0

        context.update({
            'total_recettes': current_recettes,
            'total_depenses': current_depenses,
            'net_profit': current_benefice,
            'marge_nette': (current_benefice / current_recettes * 100) if current_recettes else 0,
            'revenue_trend': ((current_recettes - previous_recettes) / previous_recettes * 100) if previous_recettes else 0,
            'expense_trend': ((current_depenses - previous_depenses) / previous_depenses * 100) if previous_depenses else 0,
            'benefice_trend': ((current_benefice - (previous_recettes - previous_depenses)) / max(previous_recettes - previous_depenses, 1) * 100) if previous_recettes or previous_depenses else 0,
            'start_date': month_start,
            'end_date': today,
        })
        return context


class FinanceReportView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'finances/rapport.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        queryset = Transaction.objects.all()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        categorie = self.request.GET.get('categorie')

        if start_date:
            queryset = queryset.filter(date_operation__gte=start_date)
        if end_date:
            queryset = queryset.filter(date_operation__lte=end_date)
        if categorie:
            queryset = queryset.filter(categorie=categorie)

        return queryset.order_by('-date_operation')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = self.request.GET.get('start_date') or date.today().replace(day=1).isoformat()
        end_date = self.request.GET.get('end_date') or date.today().isoformat()
        categorie = self.request.GET.get('categorie', '')
        queryset = self.get_queryset()

        total_recettes = queryset.filter(type_transaction='recette').aggregate(total=models.Sum('montant'))['total'] or 0
        total_depenses = queryset.filter(type_transaction='depense').aggregate(total=models.Sum('montant'))['total'] or 0
        net = total_recettes - total_depenses
        margin = (net / total_recettes * 100) if total_recettes else 0

        category_totals = (
            queryset.filter(type_transaction='depense')
            .values('categorie')
            .annotate(total=models.Sum('montant'))
            .order_by('-total')
        )
        categories = [choice for choice in Transaction.CATEGORIE_CHOICES]

        category_breakdown = []
        total_depenses_for_breakdown = sum(item['total'] or 0 for item in category_totals)
        for item in category_totals:
            category_breakdown.append({
                'categorie': dict(Transaction.CATEGORIE_CHOICES).get(item['categorie'], item['categorie']),
                'total': item['total'] or 0,
                'percent': (item['total'] / total_depenses_for_breakdown * 100) if total_depenses_for_breakdown else 0,
            })

        context.update({
            'total_recettes': total_recettes,
            'total_depenses': total_depenses,
            'net_profit': net,
            'marge_nette': margin,
            'category_breakdown': category_breakdown,
            'categories': categories,
            'selected_categorie': categorie,
            'start_date': start_date,
            'end_date': end_date,
        })
        return context


class FinanceStatsView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'finances/statistiques.html'
    context_object_name = 'transactions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        year_start = date(today.year, 1, 1)

        annual_transactions = Transaction.objects.filter(date_operation__gte=year_start, date_operation__lte=today)
        recettes = annual_transactions.filter(type_transaction='recette').aggregate(total=models.Sum('montant'))['total'] or 0
        depenses = annual_transactions.filter(type_transaction='depense').aggregate(total=models.Sum('montant'))['total'] or 0
        benefice = recettes - depenses
        recettes_count = annual_transactions.filter(type_transaction='recette').count()

        category_breakdown = (
            annual_transactions.values('categorie')
            .annotate(total=models.Sum('montant'))
            .order_by('-total')[:5]
        )
        category_breakdown_list = list(category_breakdown)
        monthly_totals = annual_transactions.values('date_operation__month', 'type_transaction').annotate(
            total=models.Sum('montant')
        )
        monthly_map = {
            (item['date_operation__month'], item['type_transaction']): float(item['total'] or 0)
            for item in monthly_totals
        }

        context.update({
            'annual_recettes': recettes,
            'annual_depenses': depenses,
            'annual_profit': benefice,
            'average_ticket': (recettes / recettes_count) if recettes_count else 0,
            'annual_transactions_count': annual_transactions.count(),
            'top_categories': [
                {
                    'categorie': dict(Transaction.CATEGORIE_CHOICES).get(item['categorie'], item['categorie']),
                    'total': item['total'] or 0,
                }
                for item in category_breakdown_list
            ],
            'category_chart_labels': [
                dict(Transaction.CATEGORIE_CHOICES).get(item['categorie'], item['categorie'])
                for item in category_breakdown_list
            ],
            'category_chart_values': [float(item['total'] or 0) for item in category_breakdown_list],
            'finance_month_labels': [f'Mois {month}' for month in range(1, 13)],
            'finance_revenue_values': [monthly_map.get((month, 'recette'), 0) for month in range(1, 13)],
            'finance_expense_values': [monthly_map.get((month, 'depense'), 0) for month in range(1, 13)],
        })
        return context
