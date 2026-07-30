from django.shortcuts import render


def liste(request):
    return render(request, 'activites/liste.html')


def calendrier(request):
    return render(request, 'activites/calendrier.html')


def detail(request, pk):
    return render(request, 'activites/detail.html', {'pk': pk})


def ajouter(request):
    return render(request, 'activites/ajouter.html')


def modifier(request, pk):
    return render(request, 'activites/modifier.html', {'pk': pk})
