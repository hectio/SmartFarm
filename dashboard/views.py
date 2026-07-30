from django.http import HttpResponse

def accueil(request):
    return HttpResponse("<h1>Bienvenue sur SmartFarm 🌱</h1><p>La plateforme intelligente de gestion des exploitations maraîchères.</p>")
