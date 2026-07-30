from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.liste_intrants, name='liste_intrants'),
    path('ajouter/', views.ajouter_intrant, name='ajouter_intrant'),
    path('entree/', views.entree_stock, name='entree_stock'),
    path('sortie/', views.sortie_stock, name='sortie_stock'),
    path('mouvements/', views.mouvements, name='mouvements'),
    path('alertes/', views.alertes, name='alertes'),
]
