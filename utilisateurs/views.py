from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import UtilisateurRegisterForm, UtilisateurUpdateForm, ProfilForm
from .models import ProfilUtilisateur

User = get_user_model()

staff_required = user_passes_test(
    lambda user: user.is_authenticated and user.is_staff,
    login_url='utilisateurs:login',
)


def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Connexion réussie !')
            return redirect('dashboard:accueil')
        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
    else:
        form = AuthenticationForm()

    return render(request, 'utilisateurs/login.html', {'form': form})


def deconnexion(request):
    logout(request)
    messages.success(request, 'Vous êtes déconnecté')
    return redirect(reverse('utilisateurs:login'))


def register(request):
    if request.method == 'POST':
        user_form = UtilisateurRegisterForm(request.POST)
        profile_form = ProfilForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Inscription réussie. Vous pouvez maintenant vous connecter.')
            return redirect('utilisateurs:login')
    else:
        user_form = UtilisateurRegisterForm()
        profile_form = ProfilForm()

    return render(request, 'utilisateurs/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def profil(request):
    profile, _ = ProfilUtilisateur.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UtilisateurUpdateForm(request.POST, instance=request.user)
        profile_form = ProfilForm(request.POST, request.FILES, instance=profile)
        password_form = PasswordChangeForm(request.user, request.POST)

        if 'update_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Mot de passe mis à jour avec succès.')
                return redirect('utilisateurs:profil')
        else:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Profil mis à jour avec succès.')
                return redirect('utilisateurs:profil')
    else:
        user_form = UtilisateurUpdateForm(instance=request.user)
        profile_form = ProfilForm(instance=profile)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'utilisateurs/profil.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    })


@staff_required
def liste(request):
    users = User.objects.select_related('profil').all()
    return render(request, 'utilisateurs/liste.html', {'users': users})


@staff_required
def ajouter(request):
    if request.method == 'POST':
        user_form = UtilisateurRegisterForm(request.POST)
        profile_form = ProfilForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Utilisateur créé avec succès.')
            return redirect('utilisateurs:liste')
    else:
        user_form = UtilisateurRegisterForm()
        profile_form = ProfilForm()

    return render(request, 'utilisateurs/ajouter.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@staff_required
def modifier(request, pk):
    utilisateur = get_object_or_404(User, pk=pk)
    profile, _ = ProfilUtilisateur.objects.get_or_create(user=utilisateur)

    if request.method == 'POST':
        user_form = UtilisateurUpdateForm(request.POST, instance=utilisateur)
        profile_form = ProfilForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Utilisateur mis à jour avec succès.')
            return redirect('utilisateurs:liste')
    else:
        user_form = UtilisateurUpdateForm(instance=utilisateur)
        profile_form = ProfilForm(instance=profile)

    return render(request, 'utilisateurs/modifier.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'utilisateur': utilisateur,
    })


@staff_required
def supprimer(request, pk):
    utilisateur = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        utilisateur.delete()
        messages.success(request, 'Utilisateur supprimé avec succès.')
        return redirect('utilisateurs:liste')
    return render(request, 'utilisateurs/supprimer.html', {'utilisateur': utilisateur})
