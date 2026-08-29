from django.test import TestCase
from django.urls import reverse


class VentesRoutesTest(TestCase):
    def test_client_list_route_exists(self):
        self.assertEqual(reverse('ventes:clients_liste'), '/ventes/clients/')

    def test_commande_list_route_exists(self):
        self.assertEqual(reverse('ventes:commandes_liste'), '/ventes/commandes/')

    def test_client_form_success_url_is_valid(self):
        self.assertEqual(reverse('ventes:clients_liste'), '/ventes/clients/')

    def test_commande_form_success_url_is_valid(self):
        self.assertEqual(reverse('ventes:commandes_liste'), '/ventes/commandes/')
