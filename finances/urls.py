from django.urls import path
from . import views

app_name = 'finances'

urlpatterns = [
    path('', views.RecetteListView.as_view(), name='recettes'),
    path('recettes/', views.RecetteListView.as_view(), name='recettes'),
    path('depenses/', views.DepenseListView.as_view(), name='depenses'),
    path('benefices/', views.FinanceBeneficeView.as_view(), name='benefices'),
    path('rapport/', views.FinanceReportView.as_view(), name='rapport'),
    path('statistiques/', views.FinanceStatsView.as_view(), name='statistiques'),
    path('nouvelle/', views.TransactionCreateView.as_view(), name='nouvelle_transaction'),
    path('<int:pk>/modifier/', views.TransactionUpdateView.as_view(), name='modifier_transaction'),
    path('<int:pk>/supprimer/', views.TransactionDeleteView.as_view(), name='supprimer_transaction'),
]
