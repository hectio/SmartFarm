from django.urls import path
from . import views

app_name = 'activites'

urlpatterns = [
    path('', views.liste, name='liste'),
    path('calendrier/', views.calendrier, name='calendrier'),
    path('ajouter/', views.ajouter, name='ajouter'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/modifier/', views.modifier, name='modifier'),
]
