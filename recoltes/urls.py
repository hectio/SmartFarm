from django.urls import path
from .views import RecolteListView, RecolteCreateView, RecolteDetailView, RecolteStatistiquesView

app_name = 'recoltes'

urlpatterns = [
    path('', RecolteListView.as_view(), name='recoltes_liste'),
    path('ajouter/', RecolteCreateView.as_view(), name='recoltes_ajouter'),
    path('statistiques/', RecolteStatistiquesView.as_view(), name='statistiques'),
    path('<int:pk>/', RecolteDetailView.as_view(), name='recoltes_detail'),
]
