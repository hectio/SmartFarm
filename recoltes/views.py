from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic import TemplateView
from datetime import date

from cultures.views import RecolteListView, RecolteCreateView, RecolteDetailView
from cultures.models import Recolte
from ventes.models import VENTE


class RecolteStatistiquesView(LoginRequiredMixin, TemplateView):
	template_name = 'recoltes/statistiques.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		today = date.today()
		year_start = date(today.year, 1, 1)
		recoltes = Recolte.objects.filter(
			date__gte=year_start,
			date__lte=today,
			unite='kg',
		).select_related('culture', 'parcelle')
		total_recolte = recoltes.aggregate(total=Sum('quantite'))['total'] or 0
		surfaces = sum(recolte.parcelle.superficie for recolte in recoltes)
		par_culture = (
			recoltes.values('culture__nom')
			.annotate(total=Sum('quantite'))
			.order_by('-total')
		)
		par_mois = (
			recoltes.values('date__month')
			.annotate(total=Sum('quantite'))
			.order_by('date__month')
		)
		context.update({
			'total_recolte': total_recolte,
			'rendement_moyen': (total_recolte / surfaces) if surfaces else 0,
			'nombre_recoltes': recoltes.count(),
			'valeur_ventes': VENTE.objects.filter(
				date_commande__gte=year_start,
				date_commande__lte=today,
			).aggregate(total=Sum('total'))['total'] or 0,
			'recoltes_par_culture': par_culture,
			'recoltes_par_mois': par_mois,
			'culture_chart_labels': [item['culture__nom'] for item in par_culture],
			'culture_chart_values': [float(item['total'] or 0) for item in par_culture],
			'month_chart_labels': [f'Mois {item["date__month"]}' for item in par_mois],
			'month_chart_values': [float(item['total'] or 0) for item in par_mois],
			'annee_statistiques': today.year,
		})
		return context

__all__ = [
	'RecolteListView',
	'RecolteCreateView',
	'RecolteDetailView',
	'RecolteStatistiquesView',
]
