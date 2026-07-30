from django.shortcuts import render


def liste(request):
    return render(request, 'ventes/liste.html')


def detail(request, pk):
    return render(request, 'ventes/detail.html', {'pk': pk})


def facture(request, pk):
    return render(request, 'ventes/facture.html', {'pk': pk})


def ajouter(request):
    return render(request, 'ventes/ajouter.html')
