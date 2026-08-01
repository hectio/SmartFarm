from django.contrib import admin

from .models import Intrant, MouvementStock


@admin.register(Intrant)
class IntrantAdmin(admin.ModelAdmin):
    list_display = ('nom', 'quantite', 'unite', 'seuil_alerte')
    search_fields = ('nom',)


@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = ('intrant', 'type_mouvement', 'quantite', 'date_mouvement', 'responsable')
    list_filter = ('type_mouvement', 'date_mouvement')
    search_fields = ('intrant__nom', 'commentaire')
