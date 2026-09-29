from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Transaction


class FinanceViewsTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='finance-user',
			password='test-password',
		)
		self.client.force_login(self.user)
		self.today = date.today()
		self.recette = Transaction.objects.create(
			type_transaction='recette',
			titre='Vente de maïs local',
			montant='150000',
			categorie='vente',
			date_operation=self.today,
		)
		self.depense = Transaction.objects.create(
			type_transaction='depense',
			titre='Achat de semences',
			montant='40000',
			categorie='achat',
			date_operation=self.today,
		)

	def test_recettes_list_filters_recettes_and_exposes_total(self):
		response = self.client.get(reverse('finances:recettes'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(list(response.context['transactions']), [self.recette])
		self.assertEqual(response.context['total_recettes'], 150000)

	def test_depenses_list_filters_depenses(self):
		response = self.client.get(reverse('finances:depenses'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(list(response.context['transactions']), [self.depense])

	def test_benefice_view_calculates_current_month_result(self):
		response = self.client.get(reverse('finances:benefices'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['total_recettes'], 150000)
		self.assertEqual(response.context['total_depenses'], 40000)
		self.assertEqual(response.context['net_profit'], 110000)

	def test_report_view_filters_by_date_and_category(self):
		old_transaction = Transaction.objects.create(
			type_transaction='recette',
			titre='Ancienne vente',
			montant='5000',
			categorie='vente',
			date_operation=self.today - timedelta(days=10),
		)
		response = self.client.get(reverse('finances:rapport'), {
			'start_date': self.today.isoformat(),
			'end_date': self.today.isoformat(),
			'categorie': 'vente',
		})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(list(response.context['transactions']), [self.recette])
		self.assertNotIn(old_transaction, response.context['transactions'])
		self.assertEqual(response.context['total_recettes'], 150000)

	def test_annual_statistics_calculates_profit_and_ticket_average(self):
		response = self.client.get(reverse('finances:statistiques'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['annual_recettes'], 150000)
		self.assertEqual(response.context['annual_depenses'], 40000)
		self.assertEqual(response.context['annual_profit'], 110000)
		self.assertEqual(response.context['average_ticket'], 150000)

	def test_transaction_creation_redirects_and_saves_fcfa_amount(self):
		response = self.client.post(reverse('finances:nouvelle_transaction'), {
			'type_transaction': 'recette',
			'titre': 'Vente de tomates',
			'description': 'Marché local',
			'montant': '27500',
			'categorie': 'vente',
			'date_operation': self.today.isoformat(),
			'responsable': self.user.pk,
		})

		self.assertRedirects(response, reverse('finances:recettes'))
		self.assertTrue(Transaction.objects.filter(titre='Vente de tomates', montant='27500').exists())

# Create your tests here.
