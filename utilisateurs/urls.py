from django.urls import path
from . import views

app_name = 'utilisateurs'

urlpatterns = [
    path('', views.connexion, name='login'),
    path('login/', views.connexion, name='login'),
    path('logout/', views.deconnexion, name='logout'),
    path('register/', views.register, name='register'),
    path('profil/', views.profil, name='profil'),
    path('liste/', views.liste, name='liste'),
    path('ajouter/', views.ajouter, name='ajouter'),
    path('modifier/<int:pk>/', views.modifier, name='modifier'),
    path('supprimer/<int:pk>/', views.supprimer, name='supprimer'),
]