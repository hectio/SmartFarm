from django.db import models
from django.contrib.auth import get_user_model

from parcelles.models import Parcelle
from cultures.models import Culture

User = get_user_model()


class Activite(models.Model):
    TYPE_CHOICES = [
        ('semis', 'Semis / Plantation'),
        ('entretien', 'Entretien'),
        ('irrigation', 'Irrigation'),
        ('recolte', 'Récolte'),
        ('ventes', 'Ventes'),
        ('transport', 'Transport'),
        ('autre', 'Autre'),
    ]

    STATUT_CHOICES = [
        ('planifie', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    titre = models.CharField(max_length=200, help_text="Titre de l'activité")
    description = models.TextField(blank=True, help_text="Description détaillée")
    type_activite = models.CharField(max_length=20, choices=TYPE_CHOICES, default='autre')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifie')
    parcelle = models.ForeignKey(
        Parcelle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activites',
        help_text="Parcelle concernée par l'activité"
    )
    culture = models.ForeignKey(
        Culture,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activites',
        help_text="Culture concernée par l'activité"
    )
    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activites',
        help_text="Responsable de l'activité"
    )
    date_debut = models.DateField(help_text="Date de début de l'activité")
    date_fin = models.DateField(null=True, blank=True, help_text="Date de fin prévue")
    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création")
    date_modification = models.DateTimeField(auto_now=True, help_text="Date de dernière modification")

    class Meta:
        ordering = ['-date_debut', 'titre']
        verbose_name = 'Activité'
        verbose_name_plural = 'Activités'

    def __str__(self):
        return f"{self.titre} ({self.get_type_activite_display()})"
