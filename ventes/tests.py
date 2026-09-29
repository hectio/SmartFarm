from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Client, VENTE, VenteArticle


class VentesRoutesTest(TestCase):
    def test_client_list_route_exists(self):
        self.assertEqual(reverse('ventes:clients_liste'), '/ventes/clients/')

    def test_commande_list_route_exists(self):
        self.assertEqual(reverse('ventes:commandes_liste'), '/ventes/commandes/')

    def test_client_form_success_url_is_valid(self):
        self.assertEqual(reverse('ventes:clients_liste'), '/ventes/clients/')

    def test_commande_form_success_url_is_valid(self):
        self.assertEqual(reverse('ventes:commandes_liste'), '/ventes/commandes/')


class VenteTotalTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='vente-user',
            password='test-password',
        )
        self.client.force_login(self.user)

    def test_total_is_calculated_from_submitted_articles(self):
        response = self.client.post(reverse('ventes:ajouter'), {
            'date_commande': '2026-09-09',
            'statut': 'confirmee',
            'description': 'Vente de tomates',
            'responsable': self.user.pk,
            'articles-TOTAL_FORMS': '1',
            'articles-INITIAL_FORMS': '0',
            'articles-MIN_NUM_FORMS': '0',
            'articles-MAX_NUM_FORMS': '1000',
            'articles-0-culture': '',
            'articles-0-parcelle': '',
            'articles-0-quantite': '2',
            'articles-0-prix_unitaire': '150',
        })

        self.assertRedirects(response, reverse('ventes:liste'))
        vente = VENTE.objects.get()
        self.assertEqual(vente.total, 300)
        self.assertEqual(VenteArticle.objects.filter(vente=vente).count(), 1)

    def test_total_is_displayed_in_sales_list(self):
        VENTE.objects.create(
            total='1234.50',
            date_commande='2026-09-09',
            client=Client.objects.create(nom='Client test'),
        )

        response = self.client.get(reverse('ventes:liste'))

        self.assertContains(response, '1234.50 CFA')

    def test_newest_sales_are_listed_first(self):
        older = VENTE.objects.create(
            total='100.00',
            date_commande='2026-09-09',
            client=Client.objects.create(nom='Client ancien'),
        )
        newer = VENTE.objects.create(
            total='200.00',
            date_commande='2026-09-09',
            client=Client.objects.create(nom='Client récent'),
        )

        response = self.client.get(reverse('ventes:liste'))
        sales = list(response.context['ventes'])

        self.assertEqual(sales[:2], [newer, older])

    def test_sale_pdf_download_returns_a_pdf_attachment(self):
        vente = VENTE.objects.create(
            total='1234.50',
            date_commande='2026-09-09',
            client=Client.objects.create(nom='Client PDF'),
        )

        response = self.client.get(reverse('ventes:facture_pdf', args=[vente.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn(f'facture-vente-{vente.pk}.pdf', response['Content-Disposition'])
        self.assertTrue(response.content.startswith(b'%PDF'))

    def test_commande_creation_saves_articles_and_total(self):
        response = self.client.post(reverse('ventes:commandes_ajouter'), {
            'date_commande': '2026-09-09',
            'statut': 'confirmee',
            'description': 'Commande de tomates',
            'responsable': self.user.pk,
            'articles-TOTAL_FORMS': '1',
            'articles-INITIAL_FORMS': '0',
            'articles-MIN_NUM_FORMS': '0',
            'articles-MAX_NUM_FORMS': '1000',
            'articles-0-culture': '',
            'articles-0-parcelle': '',
            'articles-0-quantite': '3',
            'articles-0-prix_unitaire': '200',
        })

        self.assertRedirects(response, reverse('ventes:commandes_liste'))
        commande = VENTE.objects.get()
        self.assertEqual(commande.total, 600)
        self.assertEqual(commande.articles.count(), 1)

    def test_commande_update_recalculates_total(self):
        commande = VENTE.objects.create(
            total='100.00',
            date_commande='2026-09-09',
            client=Client.objects.create(nom='Client commande'),
        )
        VenteArticle.objects.create(vente=commande, quantite='1', prix_unitaire='100')

        response = self.client.post(reverse('ventes:commandes_modifier', args=[commande.pk]), {
            'date_commande': '2026-09-10',
            'statut': 'livree',
            'description': 'Commande mise à jour',
            'responsable': self.user.pk,
            'articles-TOTAL_FORMS': '1',
            'articles-INITIAL_FORMS': '1',
            'articles-MIN_NUM_FORMS': '0',
            'articles-MAX_NUM_FORMS': '1000',
            'articles-0-id': commande.articles.get().pk,
            'articles-0-culture': '',
            'articles-0-parcelle': '',
            'articles-0-quantite': '4',
            'articles-0-prix_unitaire': '250',
        })

        self.assertRedirects(response, reverse('ventes:commandes_liste'))
        commande.refresh_from_db()
        self.assertEqual(commande.total, 1000)

    def test_commande_detail_uses_real_data(self):
        commande = VENTE.objects.create(
            total='1234.50',
            date_commande='2026-09-09',
            description='Commande réelle',
            client=Client.objects.create(nom='Client réel'),
        )

        response = self.client.get(reverse('ventes:commandes_detail', args=[commande.pk]))

        self.assertContains(response, f'CMD-{commande.pk}')
        self.assertContains(response, 'Client réel')
        self.assertContains(response, '1234.50 FCFA')
