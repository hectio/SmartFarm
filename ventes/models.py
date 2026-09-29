from django.db import models
from django.contrib.auth import get_user_model

from cultures.models import Culture
from parcelles.models import Parcelle

User = get_user_model()


class Client(models.Model):
    TYPE_CLIENT_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('commerce', 'Commerce'),
        ('particulier', 'Particulier'),
        ('entreprise', 'Entreprise'),
    ]

    nom = models.CharField(max_length=200, help_text="Nom du client")
    type_client = models.CharField(
        max_length=50,
        choices=TYPE_CLIENT_CHOICES,
        default='particulier',
        help_text="Type de client"
    )
    email = models.EmailField(blank=True, help_text="Email du client")
    telephone = models.CharField(max_length=20, blank=True, help_text="Téléphone du client")
    adresse = models.TextField(blank=True, help_text="Adresse du client")
    code_postal = models.CharField(max_length=20, blank=True, help_text="Code postal")
    ville = models.CharField(max_length=100, blank=True, help_text="Ville")
    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création")

    class Meta:
        ordering = ['nom']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return self.nom


class VENTE(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('confirmee', 'Confirmée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ventes',
        help_text="Client de la vente"
    )
    description = models.TextField(blank=True, help_text="Description de la vente")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon', help_text="Statut de la commande")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Montant total de la vente")
    date_commande = models.DateField(help_text="Date de la commande")
    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création")
    date_modification = models.DateTimeField(auto_now=True, help_text="Date de dernière modification")
    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ventes',
        help_text="Responsable de la vente"
    )

    class Meta:
        ordering = ['-date_commande', '-date_creation']
        verbose_name = 'Vente'
        verbose_name_plural = 'Ventes'

    def __str__(self):
        return f"Vente #{self.pk} - {self.client}"

    def recalculer_total(self):
        self.total = sum(article.montant_total() for article in self.articles.all())
        self.save(update_fields=['total', 'date_modification'])


class VenteArticle(models.Model):
    vente = models.ForeignKey(
        VENTE,
        on_delete=models.CASCADE,
        related_name='articles',
        help_text="Vente associée"
    )
    culture = models.ForeignKey(
        Culture,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vente_articles',
        help_text="Culture vendue"
    )
    parcelle = models.ForeignKey(
        Parcelle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vente_articles',
        help_text="Parcelle associée"
    )
    quantite = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantité vendue")
    prix_unitaire = models.DecimalField(max_digits=12, decimal_places=2, help_text="Prix unitaire")

    class Meta:
        verbose_name = 'Article de vente'
        verbose_name_plural = 'Articles de vente'

    def __str__(self):
        return f"{self.quantite} x {self.culture or self.parcelle or 'Article'}"

    def montant_total(self):
        return self.quantite * self.prix_unitaire
