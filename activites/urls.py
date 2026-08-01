from django.urls import path
from . import views

app_name = 'activites'

urlpatterns = [
    path('', views.ActiviteListView.as_view(), name='liste'),
    path('calendrier/', views.calendrier, name='calendrier'),
    path('ajouter/', views.ActiviteCreateView.as_view(), name='ajouter'),
    path('<int:pk>/', views.ActiviteDetailView.as_view(), name='detail'),
    path('<int:pk>/modifier/', views.ActiviteUpdateView.as_view(), name='modifier'),
]
