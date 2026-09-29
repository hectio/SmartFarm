from django import forms
from django.contrib.auth import get_user_model

from .models import Activite
from parcelles.models import Parcelle
from cultures.models import Culture

User = get_user_model()


class ActiviteForm(forms.ModelForm):
    class Meta:
        model = Activite
        fields = [
            'titre',
            'description',
            'type_activite',
            'statut',
            'parcelle',
            'culture',
            'responsable',
            'date_debut',
            'date_fin',
        ]
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l\'activité'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description de l\'activité'}),
            'type_activite': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'parcelle': forms.Select(attrs={'class': 'form-select'}),
            'culture': forms.Select(attrs={'class': 'form-select'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parcelle'].queryset = Parcelle.objects.all()
        self.fields['culture'].queryset = Culture.objects.select_related('parcelle').all()
        self.fields['responsable'].queryset = User.objects.all()
        self.fields['culture'].required = False
        self.fields['parcelle'].required = False
        self.fields['responsable'].required = False
        self.fields['date_fin'].required = False

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')

        if date_debut and date_fin and date_fin < date_debut:
            self.add_error('date_fin', 'La date de fin doit être postérieure ou égale à la date de début.')

        return cleaned_data
