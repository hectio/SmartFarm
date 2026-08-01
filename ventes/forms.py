from django import forms
from django.contrib.auth import get_user_model

from .models import Client, VENTE, VenteArticle

User = get_user_model()


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'nom',
            'type_client',
            'email',
            'telephone',
            'adresse',
            'code_postal',
            'ville',
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du client'}),
            'type_client': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Adresse complète'}),
            'code_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code postal'}),
            'ville': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville'}),
        }


class VenteForm(forms.ModelForm):
    class Meta:
        model = VENTE
        fields = [
            'client',
            'description',
            'statut',
            'total',
            'date_commande',
            'responsable',
        ]
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_commande': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsable'].queryset = User.objects.all()


class VenteArticleForm(forms.ModelForm):
    class Meta:
        model = VenteArticle
        fields = [
            'vente',
            'culture',
            'parcelle',
            'quantite',
            'prix_unitaire',
        ]
        widgets = {
            'vente': forms.Select(attrs={'class': 'form-select'}),
            'culture': forms.Select(attrs={'class': 'form-select'}),
            'parcelle': forms.Select(attrs={'class': 'form-select'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'prix_unitaire': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
