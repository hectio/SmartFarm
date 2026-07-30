from django.urls import path
from . import views

app_name = 'ventes'

urlpatterns = [
    path('', views.liste, name='liste'),
    path('ajouter/', views.ajouter, name='ajouter'),
    path('<int:pk>/', views.detail, name='detail'),
    path('facture/<int:pk>/', views.facture, name='facture'),
]
