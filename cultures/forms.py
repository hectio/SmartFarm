from django import forms
from .models import Culture


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
