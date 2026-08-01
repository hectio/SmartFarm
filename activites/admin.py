from django.contrib import admin

from .models import Activite


@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_activite', 'statut', 'parcelle', 'culture', 'date_debut', 'date_fin')
    list_filter = ('type_activite', 'statut', 'date_debut')
    search_fields = ('titre', 'description')
