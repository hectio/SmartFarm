from django.urls import path
from . import views

app_name = 'cultures'

urlpatterns = [
    path('', views.CultureListView.as_view(), name='liste'),
    path('calendrier/', views.calendrier, name='calendrier'),
    path('ajouter/', views.CultureCreateView.as_view(), name='ajouter'),
    path('<int:pk>/', views.CultureDetailView.as_view(), name='detail'),
    path('<int:pk>/modifier/', views.CultureUpdateView.as_view(), name='modifier'),
    path('<int:pk>/supprimer/', views.CultureDeleteView.as_view(), name='supprimer'),
]
