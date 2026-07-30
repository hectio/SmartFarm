from django.shortcuts import render


def liste_intrants(request):
    return render(request, 'stock/liste_intrants.html')


def ajouter_intrant(request):
    return render(request, 'stock/ajouter_intrant.html')


def entree_stock(request):
    return render(request, 'stock/entree_stock.html')


def sortie_stock(request):
    return render(request, 'stock/sortie_stock.html')


def mouvements(request):
    return render(request, 'stock/mouvements.html')


def alertes(request):
    return render(request, 'stock/alertes.html')
