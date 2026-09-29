from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Intrant, MouvementStock


class StockMovementTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='stock-user',
			password='test-password',
		)
		self.client.force_login(self.user)
		self.intrant = Intrant.objects.create(
			nom='Engrais',
			quantite='10.00',
			unite='kg',
			seuil_alerte='5.00',
		)

	def movement_data(self, **overrides):
		data = {
			'intrant': self.intrant.pk,
			'type_mouvement': 'sortie',
			'quantite': '2.00',
			'date_mouvement': date.today().isoformat(),
			'responsable': self.user.pk,
			'commentaire': 'Test stock',
		}
		data.update(overrides)
		return data

	def test_valid_exit_decreases_stock(self):
		response = self.client.post(
			reverse('stock:ajouter_mouvement'),
			self.movement_data(),
		)

		self.assertRedirects(response, reverse('stock:mouvements'))
		self.intrant.refresh_from_db()
		self.assertEqual(self.intrant.quantite, 8)
		self.assertEqual(MouvementStock.objects.count(), 1)

	def test_valid_entry_increases_stock(self):
		response = self.client.post(
			reverse('stock:ajouter_mouvement'),
			self.movement_data(type_mouvement='entree', quantite='4.00'),
		)

		self.assertRedirects(response, reverse('stock:mouvements'))
		self.intrant.refresh_from_db()
		self.assertEqual(self.intrant.quantite, 14)

	def test_exit_cannot_exceed_available_stock(self):
		response = self.client.post(
			reverse('stock:ajouter_mouvement'),
			self.movement_data(quantite='11.00'),
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'ne peut pas dépasser le stock disponible')
		self.intrant.refresh_from_db()
		self.assertEqual(self.intrant.quantite, 10)
		self.assertEqual(MouvementStock.objects.count(), 0)

	def test_movement_quantity_must_be_positive(self):
		response = self.client.post(
			reverse('stock:ajouter_mouvement'),
			self.movement_data(quantite='0'),
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'supérieure à zéro')
		self.assertEqual(MouvementStock.objects.count(), 0)


class StockAlertTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='alert-user',
			password='test-password',
		)
		self.client.force_login(self.user)

	def test_alerts_only_include_intrants_at_or_below_threshold(self):
		low_stock = Intrant.objects.create(nom='Stock bas', quantite='3', seuil_alerte='5')
		Intrant.objects.create(nom='Stock suffisant', quantite='8', seuil_alerte='5')

		response = self.client.get(reverse('stock:alertes'))

		self.assertEqual(list(response.context['intrants']), [low_stock])
		self.assertEqual(response.context['intrants'][0].ecart, 2)

	def test_movement_detail_route_displays_movement(self):
		mouvement = MouvementStock.objects.create(
			intrant=Intrant.objects.create(nom='Semences', quantite='10', seuil_alerte='2'),
			type_mouvement='entree',
			quantite='3',
			date_mouvement=date.today(),
		)

		response = self.client.get(reverse('stock:mouvement_detail', args=[mouvement.pk]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Semences')
		self.assertContains(response, '3')
