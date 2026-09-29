from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from exploitation.models import Exploitation
from parcelles.models import Parcelle
from cultures.models import Culture, Recolte


class RecolteFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='agri_test',
            email='agri@example.com',
            password='secret123',
            is_staff=True,
        )
        self.exploitation = Exploitation.objects.create(
            nom='Exploitation Test',
            responsable=self.user,
            adresse='Rue test',
            contact_email='test@example.com',
            contact_telephone='00000000',
        )
        self.parcelle = Parcelle.objects.create(
            nom='Parcelle Test',
            code='PT-001',
            superficie=200,
            type_sol='mixte',
            irrigation=True,
            exploitation=self.exploitation,
            statut='actif',
        )
        self.culture = Culture.objects.create(
            nom='Tomates',
            variete='Cherry',
            parcelle=self.parcelle,
            date_semis=timezone.now().date(),
            date_prevision_recolte=timezone.now().date(),
            rendement_attendu=4.5,
            statut='en_croissance',
        )

    def test_recoltes_list_requires_login(self):
        response = self.client.get(reverse('recoltes:recoltes_liste'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_create_recolte(self):
        self.client.login(username='agri_test', password='secret123')
        today = timezone.now().date()

        response = self.client.post(
            reverse('recoltes:recoltes_ajouter'),
            {
                'date': today.isoformat(),
                'culture': self.culture.pk,
                'parcelle': self.parcelle.pk,
                'quantite': '42.5',
                'unite': 'kg',
                'qualite': 'bonne',
                'notes': 'Première récolte de test',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Recolte.objects.filter(notes='Première récolte de test').exists())

    def test_recolte_statistics_route_requires_login(self):
        response = self.client.get(reverse('recoltes:statistiques'))

        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_view_recolte_statistics(self):
        self.client.login(username='agri_test', password='secret123')

        response = self.client.get(reverse('recoltes:statistiques'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Statistiques des Récoltes')

    def test_recolte_statistics_uses_real_quantities_and_sales(self):
        self.client.login(username='agri_test', password='secret123')
        Recolte.objects.create(
            date=timezone.now().date(),
            culture=self.culture,
            parcelle=self.parcelle,
            quantite='75',
            unite='kg',
        )

        response = self.client.get(reverse('recoltes:statistiques'))

        self.assertEqual(response.context['total_recolte'], 75)
        self.assertEqual(response.context['nombre_recoltes'], 1)
