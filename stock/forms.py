from django import forms
from django.contrib.auth import get_user_model

from .models import Intrant, MouvementStock

User = get_user_model()


class IntrantForm(forms.ModelForm):
    class Meta:
        model = Intrant
        fields = ['nom', 'description', 'quantite', 'unite', 'seuil_alerte']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'intrant'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description de l\'intrant'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unite': forms.Select(attrs={'class': 'form-select'}),
            'seuil_alerte': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class MouvementStockForm(forms.ModelForm):
    class Meta:
        model = MouvementStock
        fields = ['intrant', 'type_mouvement', 'quantite', 'date_mouvement', 'responsable', 'commentaire']
        widgets = {
            'intrant': forms.Select(attrs={'class': 'form-select'}),
            'type_mouvement': forms.Select(attrs={'class': 'form-select'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_mouvement': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsable'].queryset = User.objects.all()

    def clean_quantite(self):
        quantite = self.cleaned_data['quantite']
        if quantite <= 0:
            raise forms.ValidationError('La quantité doit être supérieure à zéro.')
        return quantite
