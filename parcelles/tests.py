from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Parcelle
from exploitation.models import Exploitation


class ParcelleModelTestCase(TestCase):
    """
    Tests pour le modèle Parcelle.
    """
    
    def setUp(self):
        """Créer les données de test."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.exploitation = Exploitation.objects.create(
            nom='Ferme Test',
            description='Une ferme de test'
        )
    
    def test_create_parcelle(self):
        """Tester la création d'une parcelle."""
        parcelle = Parcelle.objects.create(
            nom='Parcelle Test',
            code='TEST001',
            superficie=1000,
            type_sol='limoneux',
            exploitation=self.exploitation
        )
        self.assertEqual(parcelle.nom, 'Parcelle Test')
        self.assertEqual(parcelle.code, 'TEST001')
        self.assertEqual(parcelle.statut, 'actif')
    
    def test_parcelle_str(self):
        """Tester la représentation en string d'une parcelle."""
        parcelle = Parcelle.objects.create(
            nom='Parcelle Test',
            code='TEST002',
            superficie=500,
            exploitation=self.exploitation
        )
        self.assertEqual(str(parcelle), 'Parcelle Test (TEST002)')


class ParcelleViewsTestCase(TestCase):
    """
    Tests pour les vues de Parcelle.
    """
    
    def setUp(self):
        """Créer les données de test et l'utilisateur de test."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.exploitation = Exploitation.objects.create(
            nom='Ferme Test',
            description='Une ferme de test'
        )
        self.parcelle = Parcelle.objects.create(
            nom='Parcelle Test',
            code='TEST003',
            superficie=1500,
            exploitation=self.exploitation
        )
    
    def test_parcelle_list_view(self):
        """Tester la vue de liste des parcelles."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/parcelles/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Parcelle Test')
    
    def test_parcelle_detail_view(self):
        """Tester la vue de détail d'une parcelle."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('parcelles:parcelle_detail', kwargs={'pk': self.parcelle.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Parcelle Test')

    def test_parcelle_list_view_requires_login(self):
        """Vérifier que la liste des parcelles nécessite une connexion."""
        response = self.client.get(reverse('parcelles:parcelle_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_parcelle_create_view(self):
        """Tester la création d'une nouvelle parcelle via la vue."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('parcelles:parcelle_create'), {
            'nom': 'Parcelle Crée',
            'code': 'TEST004',
            'superficie': '2000',
            'exploitation': self.exploitation.id,
            'type_sol': 'argileux',
            'statut': 'actif',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Parcelle.objects.filter(code='TEST004').exists())

    def test_parcelle_update_view(self):
        """Tester la modification d'une parcelle existante."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('parcelles:parcelle_update', kwargs={'pk': self.parcelle.id}), {
            'nom': 'Parcelle Modifiée',
            'code': self.parcelle.code,
            'superficie': '1500',
            'exploitation': self.exploitation.id,
            'type_sol': 'sableux',
            'statut': 'actif',
        })
        self.assertEqual(response.status_code, 302)
        self.parcelle.refresh_from_db()
        self.assertEqual(self.parcelle.nom, 'Parcelle Modifiée')
        self.assertEqual(self.parcelle.type_sol, 'sableux')

    def test_parcelle_delete_view(self):
        """Tester la suppression d'une parcelle via la vue."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('parcelles:parcelle_delete', kwargs={'pk': self.parcelle.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Parcelle.objects.filter(id=self.parcelle.id).exists())
