from django.urls import path
from .views import RecolteListView, RecolteCreateView, RecolteDetailView

app_name = 'recoltes'

urlpatterns = [
    path('', RecolteListView.as_view(), name='recoltes_liste'),
    path('ajouter/', RecolteCreateView.as_view(), name='recoltes_ajouter'),
    path('<int:pk>/', RecolteDetailView.as_view(), name='recoltes_detail'),
]
