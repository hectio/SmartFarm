from django.urls import path
from . import views

app_name = 'ventes'

urlpatterns = [
    path('', views.VenteListView.as_view(), name='liste'),
    path('ajouter/', views.VenteCreateView.as_view(), name='ajouter'),
    path('<int:pk>/', views.VenteDetailView.as_view(), name='detail'),
    path('<int:pk>/modifier/', views.VenteUpdateView.as_view(), name='modifier'),
    path('facture/<int:pk>/', views.FactureDetailView.as_view(), name='facture'),

    # Clients
    path('clients/', views.ClientListView.as_view(), name='clients_liste'),
    path('clients/ajouter/', views.ClientCreateView.as_view(), name='clients_ajouter'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='clients_detail'),
    path('clients/<int:pk>/modifier/', views.ClientUpdateView.as_view(), name='clients_modifier'),

    # Commandes
    path('commandes/', views.CommandeListView.as_view(), name='commandes_liste'),
    path('commandes/ajouter/', views.CommandeCreateView.as_view(), name='commandes_ajouter'),
    path('commandes/<int:pk>/', views.CommandeDetailView.as_view(), name='commandes_detail'),
    path('commandes/<int:pk>/modifier/', views.CommandeUpdateView.as_view(), name='commandes_modifier'),
    path('commandes/facture/<int:pk>/', views.CommandeFactureView.as_view(), name='commandes_facture'),
]
