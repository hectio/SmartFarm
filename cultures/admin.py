from django.contrib import admin

from .models import Culture, Recolte


@admin.register(Culture)
class CultureAdmin(admin.ModelAdmin):
    list_display = ('nom', 'variete', 'parcelle', 'date_semis', 'date_prevision_recolte', 'statut')
    list_filter = ('statut', 'parcelle')
    search_fields = ('nom', 'variete', 'parcelle__nom')


@admin.register(Recolte)
class RecolteAdmin(admin.ModelAdmin):
    list_display = ('date', 'culture', 'parcelle', 'quantite', 'unite', 'qualite')
    list_filter = ('unite', 'qualite', 'date')
    search_fields = ('culture__nom', 'parcelle__nom')
