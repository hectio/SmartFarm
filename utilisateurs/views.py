from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def connexion(request):
    """
    Vue de connexion utilisateur
    """

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        utilisateur = authenticate(
            request,
            username=username,
            password=password
        )

        if utilisateur is not None:
            login(request, utilisateur)
            messages.success(request, "Connexion réussie !")

            return redirect('dashboard:accueil')

        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")

    return render(request, 'utilisateurs/login.html')


def deconnexion(request):
    """
    Déconnexion utilisateur
    """

    logout(request)

    messages.success(request, "Vous êtes déconnecté")

    return redirect('login')


@login_required
def profil(request):
    """
    Profil de l'utilisateur connecté
    """

    return render(
        request,
        'utilisateurs/profil.html'
    )
