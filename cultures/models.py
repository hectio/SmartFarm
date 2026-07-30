from django.db import models
from parcelles.models import Parcelle


class Culture(models.Model):
    """Modèle représentant une culture gérée sur une parcelle."""

    STATUT_CHOICES = [
        ('en_croissance', 'En croissance'),
        ('mature', 'Mature'),
        ('recolte', 'Récolte'),
        ('terminee', 'Terminée'),
    ]

    nom = models.CharField(
        max_length=150,
        help_text="Nom de la culture"
    )
    variete = models.CharField(
        max_length=150,
        help_text="Variété de la culture"
    )
    parcelle = models.ForeignKey(
        Parcelle,
        on_delete=models.CASCADE,
        related_name='cultures',
        help_text="Parcelle associée à la culture"
    )
    date_semis = models.DateField(
        help_text="Date de semis ou de plantation"
    )
    date_prevision_recolte = models.DateField(
        help_text="Date prévue de récolte"
    )
    rendement_attendu = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Rendement attendu en kg/m²"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_croissance',
        help_text="Statut actuel de la culture"
    )
    notes = models.TextField(
        blank=True,
        help_text="Notes supplémentaires sur la culture"
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        help_text="Date de création de l'enregistrement"
    )
    date_modification = models.DateTimeField(
        auto_now=True,
        help_text="Date de dernière modification de l'enregistrement"
    )

    class Meta:
        ordering = ['-date_semis']
        verbose_name = 'Culture'
        verbose_name_plural = 'Cultures'
        db_table = 'cultures_culture'

    def __str__(self):
        return f"{self.nom} ({self.variete})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('cultures:detail', kwargs={'pk': self.pk})

    def duree_croissance(self):
        return (self.date_prevision_recolte - self.date_semis).days
