from django.urls import path
from . import views

app_name = 'parcelles'

urlpatterns = [
    # Lister les parcelles
    path('', views.ParcelleListView.as_view(), name='parcelle_list'),
    
    # Voir les détails d'une parcelle
    path('<int:pk>/', views.ParcelleDetailView.as_view(), name='parcelle_detail'),
    
    # Créer une nouvelle parcelle
    path('ajouter/', views.ParcelleCreateView.as_view(), name='parcelle_create'),
    
    # Modifier une parcelle
    path('<int:pk>/modifier/', views.ParcelleUpdateView.as_view(), name='parcelle_update'),
    
    # Supprimer une parcelle
    path('<int:pk>/supprimer/', views.ParcelleDeleteView.as_view(), name='parcelle_delete'),
]
