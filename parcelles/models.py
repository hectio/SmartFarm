from django.db import models
from django.contrib.auth.models import User
from exploitation.models import Exploitation


class Parcelle(models.Model):
    """
    Modèle représentant une parcelle agricole.
    Une parcelle est une surface de terrain cultivable appartenant à une exploitation.
    """
    
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('en_preparation', 'En préparation'),
        ('reposante', 'Reposante'),
        ('suspendu', 'Suspendu'),
    ]
    
    TYPE_SOL_CHOICES = [
        ('argileux', 'Argileux'),
        ('sableux', 'Sableux'),
        ('limoneux', 'Limoneux'),
        ('calcaire', 'Calcaire'),
        ('organique', 'Organique'),
        ('mixte', 'Mixte'),
    ]
    
    nom = models.CharField(
        max_length=100,
        help_text="Nom ou identifiant de la parcelle"
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Code unique de la parcelle"
    )
    superficie = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Superficie en m² ou hectares"
    )
    type_sol = models.CharField(
        max_length=50,
        choices=TYPE_SOL_CHOICES,
        default='mixte',
        help_text="Type de sol de la parcelle"
    )
    irrigation = models.BooleanField(
    default=False,
    help_text="Indique si la parcelle dispose d'un système d'irrigation"
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Latitude GPS"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Longitude GPS"
    )
    description = models.TextField(
        blank=True,
        help_text="Description détaillée de la parcelle"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='actif',
        help_text="Statut actuel de la parcelle"
    )
    exploitation = models.ForeignKey(
        Exploitation,
        on_delete=models.CASCADE,
        related_name='parcelles',
        help_text="Exploitation à laquelle appartient cette parcelle"
    )
    photo = models.ImageField(
    upload_to='parcelles/',
    blank=True,
    null=True,
    help_text="Photo de la parcelle"
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        help_text="Date et heure de création de la parcelle"
    )
    date_modification = models.DateTimeField(
        auto_now=True,
        help_text="Date et heure de dernière modification"
    )
    
    class Meta:
        ordering = ['nom']
        verbose_name = 'Parcelle'
        verbose_name_plural = 'Parcelles'
        db_table = 'parcelles_parcelle'
    
    def __str__(self):
        return f"{self.nom} ({self.code})"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('parcelles:parcelle_detail', kwargs={'pk': self.pk})
