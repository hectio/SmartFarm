from django.shortcuts import render


def recettes(request):
    return render(request, 'finances/recettes.html')


def depenses(request):
    return render(request, 'finances/depenses.html')


def benefices(request):
    return render(request, 'finances/benefices.html')


def rapport(request):
    return render(request, 'finances/rapport.html')


def statistiques(request):
    return render(request, 'finances/statistiques.html')
