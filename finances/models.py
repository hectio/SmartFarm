from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('recette', 'Recette'),
        ('depense', 'Dépense'),
    ]
    CATEGORIE_CHOICES = [
        ('vente', 'Vente'),
        ('subvention', 'Subvention'),
        ('achat', 'Achat'),
        ('salaires', 'Salaires'),
        ('entretien', 'Entretien'),
        ('autre', 'Autre'),
    ]

    type_transaction = models.CharField(max_length=10, choices=TYPE_CHOICES, help_text="Type de transaction")
    titre = models.CharField(max_length=200, help_text="Titre de la transaction")
    description = models.TextField(blank=True, help_text="Description détaillée")
    montant = models.DecimalField(max_digits=12, decimal_places=2, help_text="Montant de la transaction")
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, default='autre', help_text="Catégorie financière")
    date_operation = models.DateField(help_text="Date de la transaction")
    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
        help_text="Utilisateur responsable de la transaction"
    )
    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création")
    date_modification = models.DateTimeField(auto_now=True, help_text="Date de dernière modification")

    class Meta:
        ordering = ['-date_operation', '-date_creation']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return f"{self.get_type_transaction_display()} - {self.titre} ({self.montant})"
