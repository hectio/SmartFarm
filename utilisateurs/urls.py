from django.urls import path
from . import views

app_name = 'utilisateurs'

urlpatterns = [

    path(
        '',
        views.connexion,
        name='login'
    ),

    path(
        'login/',
        views.connexion,
        name='login'
    ),

    path(
        'logout/',
        views.deconnexion,
        name='logout'
    ),

    path(
        'profil/',
        views.profil,
        name='profil'
    ),

]
