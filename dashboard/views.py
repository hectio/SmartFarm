from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import F, Q, Sum

from exploitation.models import Exploitation
from parcelles.models import Parcelle
from cultures.models import Culture, Recolte
from finances.models import Transaction
from stock.models import Intrant
from ventes.models import VENTE


@login_required
def accueil(request):
    total_exploitations = Exploitation.objects.count()
    total_parcelles_actives = Parcelle.objects.filter(statut='actif').count()
    total_cultures = Culture.objects.count()
    total_recoltes_prevues = Culture.objects.filter(date_prevision_recolte__gte=date.today()).count()
    recent_cultures = Culture.objects.select_related('parcelle').order_by('-date_semis')[:5]
    stock_alertes = Intrant.objects.filter(
        seuil_alerte__isnull=False,
        quantite__lte=F('seuil_alerte'),
    ).order_by('quantite')[:5]
    recoltes_proches = Culture.objects.filter(
        date_prevision_recolte__gte=date.today(),
        date_prevision_recolte__lte=date.today() + timedelta(days=7),
    ).order_by('date_prevision_recolte')[:5]

    context = {
        'total_exploitations': total_exploitations,
        'total_parcelles_actives': total_parcelles_actives,
        'total_cultures': total_cultures,
        'total_recoltes_prevues': total_recoltes_prevues,
        'recent_cultures': recent_cultures,
        'stock_alertes': stock_alertes,
        'recoltes_proches': recoltes_proches,
    }

    return render(request, 'dashboard/accueil.html', context)


@login_required
def statistiques(request):
    today = date.today()
    year_start = date(today.year, 1, 1)
    recoltes_kg = Recolte.objects.filter(date__gte=year_start, date__lte=today, unite='kg')
    ventes = VENTE.objects.filter(date_commande__gte=year_start, date_commande__lte=today)
    depenses = Transaction.objects.filter(
        type_transaction='depense',
        date_operation__gte=year_start,
        date_operation__lte=today,
    )

    total_production = recoltes_kg.aggregate(total=Sum('quantite'))['total'] or 0
    total_surface = Parcelle.objects.filter(cultures__recoltes__in=recoltes_kg).distinct().aggregate(
        total=Sum('superficie')
    )['total'] or 0
    cultures_stats = (
        Culture.objects.select_related('parcelle')
        .filter(recoltes__in=recoltes_kg)
        .annotate(production=Sum('recoltes__quantite', filter=Q(recoltes__in=recoltes_kg)))
        .order_by('parcelle__nom', 'nom')
    )
    detail_parcelles = [
        {
            'culture': culture,
            'production': culture.production or 0,
            'rendement': (culture.production / culture.parcelle.superficie)
            if culture.parcelle.superficie else 0,
        }
        for culture in cultures_stats
    ]
    monthly_sales = ventes.values('date_commande__month').annotate(total=Sum('total'))
    monthly_sales_map = {item['date_commande__month']: float(item['total'] or 0) for item in monthly_sales}
    monthly_harvests = recoltes_kg.values('date__month').annotate(total=Sum('quantite'))
    monthly_harvest_map = {item['date__month']: float(item['total'] or 0) for item in monthly_harvests}
    context = {
        'total_production': total_production,
        'rendement_moyen': (total_production / total_surface) if total_surface else 0,
        'chiffre_affaires': ventes.aggregate(total=Sum('total'))['total'] or 0,
        'cout_production': depenses.aggregate(total=Sum('montant'))['total'] or 0,
        'detail_parcelles': detail_parcelles,
        'production_labels': [culture['culture'].nom for culture in detail_parcelles],
        'production_values': [float(culture['production']) for culture in detail_parcelles],
        'monthly_labels': [
            'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
            'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre',
        ],
        'monthly_sales_values': [monthly_sales_map.get(month, 0) for month in range(1, 13)],
        'monthly_harvest_values': [monthly_harvest_map.get(month, 0) for month in range(1, 13)],
        'annee_statistiques': today.year,
    }
    return render(request, 'dashboard/statistiques.html', context)
