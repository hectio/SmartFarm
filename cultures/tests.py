from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from parcelles.models import Parcelle
from exploitation.models import Exploitation
from .models import Culture


class CultureModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.exploitation = Exploitation.objects.create(nom='Ferme Test', description='Une ferme de test')
        self.parcelle = Parcelle.objects.create(
            nom='Parcelle Test',
            code='PTEST001',
            superficie=1200,
            exploitation=self.exploitation,
        )

    def test_create_culture(self):
        culture = Culture.objects.create(
            nom='Tomates',
            variete='Roma VF',
            parcelle=self.parcelle,
            date_semis=date(2026, 5, 15),
            date_prevision_recolte=date(2026, 8, 20),
            rendement_attendu=3.5,
            statut='en_croissance',
        )
        self.assertEqual(str(culture), 'Tomates (Roma VF)')
        self.assertEqual(culture.statut, 'en_croissance')
        self.assertEqual(culture.duree_croissance(), 97)


class CultureViewsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.exploitation = Exploitation.objects.create(nom='Ferme Test', description='Une ferme de test')
        self.parcelle = Parcelle.objects.create(
            nom='Parcelle Test',
            code='PTEST002',
            superficie=1500,
            exploitation=self.exploitation,
        )
        self.culture = Culture.objects.create(
            nom='Tomates',
            variete='Roma VF',
            parcelle=self.parcelle,
            date_semis=date(2026, 5, 15),
            date_prevision_recolte=date(2026, 8, 20),
            rendement_attendu=3.5,
            statut='en_croissance',
        )

    def test_list_view_requires_login(self):
        response = self.client.get(reverse('cultures:liste'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('cultures:liste'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tomates')

    def test_detail_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('cultures:detail', kwargs={'pk': self.culture.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tomates')

    def test_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('cultures:ajouter'), {
            'nom': 'Salades',
            'variete': 'Batavia',
            'parcelle': self.parcelle.id,
            'date_semis': '2026-06-01',
            'date_prevision_recolte': '2026-07-15',
            'rendement_attendu': '2.2',
            'statut': 'mature',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Culture.objects.filter(nom='Salades').exists())

    def test_update_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('cultures:modifier', kwargs={'pk': self.culture.id}), {
            'nom': 'Tomates Modifiées',
            'variete': 'Roma VF',
            'parcelle': self.parcelle.id,
            'date_semis': '2026-05-15',
            'date_prevision_recolte': '2026-08-25',
            'rendement_attendu': '4.1',
            'statut': 'mature',
        })
        self.assertEqual(response.status_code, 302)
        self.culture.refresh_from_db()
        self.assertEqual(self.culture.nom, 'Tomates Modifiées')
        self.assertEqual(self.culture.statut, 'mature')

    def test_delete_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('cultures:supprimer', kwargs={'pk': self.culture.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Culture.objects.filter(id=self.culture.id).exists())
