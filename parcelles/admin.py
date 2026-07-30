from django.contrib import admin
from .models import Parcelle


@admin.register(Parcelle)
class ParcelleAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Parcelle.
    """
    list_display = ('code', 'nom', 'exploitation', 'type_sol', 'statut', 'superficie', 'date_creation')
    list_filter = ('statut', 'type_sol', 'exploitation', 'date_creation')
    search_fields = ('code', 'nom', 'description')
    readonly_fields = ('date_creation', 'date_modification')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'code', 'exploitation')
        }),
        ('Caractéristiques', {
            'fields': ('superficie', 'type_sol', 'statut')
        }),
        ('Localisation', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-date_creation',)
