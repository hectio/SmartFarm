from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.IntrantListView.as_view(), name='liste_intrants'),
    path('ajouter/', views.IntrantCreateView.as_view(), name='ajouter_intrant'),
    path('<int:pk>/modifier/', views.IntrantUpdateView.as_view(), name='modifier_intrant'),
    path('mouvements/', views.MouvementStockListView.as_view(), name='mouvements'),
    path('mouvements/ajouter/', views.MouvementStockCreateView.as_view(), name='ajouter_mouvement'),
    path('alertes/', views.AlerteStockView.as_view(), name='alertes'),
]
