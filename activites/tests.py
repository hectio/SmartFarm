from django.contrib.auth import get_user_model
from django.test import TestCase

from .forms import ActiviteForm
from .models import Activite


class ActiviteFormTests(TestCase):
	def test_rejects_end_date_before_start_date(self):
		form = ActiviteForm(data={
			'titre': 'Arrosage',
			'type_activite': 'irrigation',
			'statut': 'planifie',
			'date_debut': '2026-09-10',
			'date_fin': '2026-09-09',
		})

		self.assertFalse(form.is_valid())
		self.assertIn('date_fin', form.errors)

	def test_accepts_valid_activity_data(self):
		form = ActiviteForm(data={
			'titre': 'Arrosage',
			'type_activite': 'irrigation',
			'statut': 'planifie',
			'date_debut': '2026-09-09',
			'date_fin': '2026-09-10',
		})

		self.assertTrue(form.is_valid(), form.errors)


class ActiviteCreateViewTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username='test-user',
			password='test-password',
		)
		self.client.force_login(self.user)

	def test_creates_activity_with_form_field_names(self):
		response = self.client.post('/activites/ajouter/', {
			'titre': 'Semis de maïs',
			'type_activite': 'semis',
			'statut': 'planifie',
			'date_debut': '2026-09-09',
			'date_fin': '2026-09-10',
		})

		self.assertRedirects(response, '/activites/')
		self.assertTrue(Activite.objects.filter(titre='Semis de maïs').exists())
