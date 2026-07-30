from django import forms
from .models import Parcelle


class ParcelleForm(forms.ModelForm):
    """
    Formulaire pour créer et modifier une parcelle.
    """
    
    class Meta:
        model = Parcelle
        fields = ['nom', 'code', 'superficie', 'type_sol', 'latitude', 'longitude', 'description', 'statut', 'exploitation']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la parcelle'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code unique'
            }),
            'superficie': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Superficie en m² ou ha',
                'step': '0.01'
            }),
            'type_sol': forms.Select(attrs={
                'class': 'form-select'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Latitude',
                'step': '0.000001'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Longitude',
                'step': '0.000001'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description de la parcelle',
                'rows': 4
            }),
            'statut': forms.Select(attrs={
                'class': 'form-select'
            }),
            'exploitation': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
