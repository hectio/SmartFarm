from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_transaction', 'montant', 'categorie', 'date_operation', 'responsable')
    list_filter = ('type_transaction', 'categorie', 'date_operation')
    search_fields = ('titre', 'description')
