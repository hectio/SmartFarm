from django.contrib import admin
from .models import ProfilUtilisateur


@admin.register(ProfilUtilisateur)
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'exploitation', 'telephone')
    search_fields = ('user__username', 'user__email', 'role', 'exploitation')
    list_filter = ('role',)
