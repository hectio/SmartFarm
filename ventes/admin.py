from django.contrib import admin

from .models import Client, VENTE, VenteArticle


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'date_creation')
    search_fields = ('nom', 'email', 'telephone')


@admin.register(VENTE)
class VenteAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'statut', 'total', 'date_commande', 'responsable')
    list_filter = ('statut', 'date_commande')
    search_fields = ('client__nom', 'description')


@admin.register(VenteArticle)
class VenteArticleAdmin(admin.ModelAdmin):
    list_display = ('vente', 'culture', 'parcelle', 'quantite', 'prix_unitaire')
    search_fields = ('vente__id', 'culture__nom', 'parcelle__nom')
