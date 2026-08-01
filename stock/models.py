from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Intrant(models.Model):
    UNITE_CHOICES = [
        ('kg', 'Kilogramme'),
        ('g', 'Gramme'),
        ('l', 'Litre'),
        ('unite', 'Unité'),
        ('m2', 'Mètres carrés'),
        ('m3', 'Mètres cubes'),
    ]

    nom = models.CharField(max_length=150, help_text="Nom de l'intrant")
    description = models.TextField(blank=True, help_text="Description de l'intrant")
    quantite = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Quantité disponible")
    unite = models.CharField(max_length=10, choices=UNITE_CHOICES, default='kg', help_text="Unité de mesure")
    seuil_alerte = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Seuil de stock bas")
    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création")
    date_modification = models.DateTimeField(auto_now=True, help_text="Date de dernière modification")

    class Meta:
        verbose_name = 'Intrant'
        verbose_name_plural = 'Intrants'
        ordering = ['nom']

    def __str__(self):
        return self.nom


class MouvementStock(models.Model):
    TYPE_CHOICES = [
        ('entree', 'Entrée'),
        ('sortie', 'Sortie'),
    ]

    intrant = models.ForeignKey(
        Intrant,
        on_delete=models.CASCADE,
        related_name='mouvements',
        help_text="Intrant concerné par le mouvement"
    )
    type_mouvement = models.CharField(max_length=10, choices=TYPE_CHOICES, help_text="Type de mouvement")
    quantite = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantité mouvementée")
    date_mouvement = models.DateField(help_text="Date du mouvement")
    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mouvements_stock',
        help_text="Utilisateur responsable du mouvement"
    )
    commentaire = models.TextField(blank=True, help_text="Commentaire sur le mouvement")
    date_creation = models.DateTimeField(auto_now_add=True, help_text="Date de création")

    class Meta:
        verbose_name = 'Mouvement de stock'
        verbose_name_plural = 'Mouvements de stock'
        ordering = ['-date_mouvement']

    def __str__(self):
        return f"{self.get_type_mouvement_display()} - {self.intrant.nom} ({self.quantite} {self.intrant.unite})"
