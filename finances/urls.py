from django.urls import path
from . import views

app_name = 'finances'

urlpatterns = [
    path('', views.recettes, name='recettes'),
    path('recettes/', views.recettes, name='recettes'),
    path('depenses/', views.depenses, name='depenses'),
    path('benefices/', views.benefices, name='benefices'),
    path('rapport/', views.rapport, name='rapport'),
    path('statistiques/', views.statistiques, name='statistiques'),
]
