from django import forms
from .models import Culture, Recolte


class CultureForm(forms.ModelForm):
    class Meta:
        model = Culture
        fields = [
            'nom',
            'variete',
            'parcelle',
            'date_semis',
            'date_prevision_recolte',
            'rendement_attendu',
            'statut',
            'notes',
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la culture'}),
            'variete': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Variété'}),
            'parcelle': forms.Select(attrs={'class': 'form-select'}),
            'date_semis': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_prevision_recolte': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'rendement_attendu': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class RecolteForm(forms.ModelForm):
    class Meta:
        model = Recolte
        fields = [
            'date',
            'culture',
            'parcelle',
            'quantite',
            'unite',
            'qualite',
            'notes',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'culture': forms.Select(attrs={'class': 'form-select'}),
            'parcelle': forms.Select(attrs={'class': 'form-select'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unite': forms.Select(attrs={'class': 'form-select'}),
            'qualite': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
