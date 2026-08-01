from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from exploitation.models import Exploitation
from parcelles.models import Parcelle
from cultures.models import Culture


@login_required
def accueil(request):
    total_exploitations = Exploitation.objects.count()
    total_parcelles_actives = Parcelle.objects.filter(statut='actif').count()
    total_cultures = Culture.objects.count()
    total_recoltes_prevues = Culture.objects.filter(date_prevision_recolte__gte=date.today()).count()
    recent_cultures = Culture.objects.select_related('parcelle').order_by('-date_semis')[:5]

    context = {
        'total_exploitations': total_exploitations,
        'total_parcelles_actives': total_parcelles_actives,
        'total_cultures': total_cultures,
        'total_recoltes_prevues': total_recoltes_prevues,
        'recent_cultures': recent_cultures,
    }

    return render(request, 'dashboard/accueil.html', context)
