from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from exploitation.models import Exploitation
from parcelles.models import Parcelle
from cultures.models import Culture
from cultures.models import Recolte
from finances.models import Transaction
from ventes.models import Client, VENTE


class DashboardViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.exploitation = Exploitation.objects.create(nom='Ferme Test')
        self.parcelle = Parcelle.objects.create(
            nom='Parcelle Test',
            code='TEST001',
            superficie=1000,
            exploitation=self.exploitation,
        )
        self.culture = Culture.objects.create(
            nom='Tomates',
            variete='Cherry',
            parcelle=self.parcelle,
            date_semis=date.today(),
            date_prevision_recolte=date.today(),
        )

    def test_dashboard_access_requires_login(self):
        response = self.client.get(reverse('dashboard:accueil'))
        self.assertNotEqual(response.status_code, 200)
        self.assertIn('/login/', response.url)

    def test_dashboard_renders_with_counts(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('dashboard:accueil'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tableau de Bord')
        self.assertEqual(response.context['total_exploitations'], 1)
        self.assertEqual(response.context['total_parcelles_actives'], 1)
        self.assertEqual(response.context['total_cultures'], 1)
        self.assertEqual(response.context['total_recoltes_prevues'], 1)
        self.assertEqual(len(response.context['recent_cultures']), 1)

    def test_dashboard_statistics_route_requires_login(self):
        response = self.client.get(reverse('dashboard:statistiques'))

        self.assertRedirects(
            response,
            f'/login/?next={reverse("dashboard:statistiques")}',
        )

    def test_dashboard_statistics_route_renders_for_authenticated_user(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('dashboard:statistiques'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Statistiques')

    def test_dashboard_statistics_uses_real_togo_data(self):
        Recolte.objects.create(
            date=date.today(),
            culture=self.culture,
            parcelle=self.parcelle,
            quantite='120',
            unite='kg',
        )
        VENTE.objects.create(
            client=Client.objects.create(nom='Client Togo'),
            date_commande=date.today(),
            total='150000',
        )
        Transaction.objects.create(
            type_transaction='depense',
            titre='Semences locales',
            montant='25000',
            date_operation=date.today(),
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse('dashboard:statistiques'))

        self.assertEqual(response.context['total_production'], 120)
        self.assertEqual(response.context['chiffre_affaires'], 150000)
        self.assertEqual(response.context['cout_production'], 25000)
