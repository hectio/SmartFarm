from django import forms
from django.contrib.auth import get_user_model

from .models import Transaction

User = get_user_model()


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'type_transaction',
            'titre',
            'description',
            'montant',
            'categorie',
            'date_operation',
            'responsable',
        ]
        widgets = {
            'type_transaction': forms.Select(attrs={'class': 'form-select'}),
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de la transaction'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'date_operation': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsable'].queryset = User.objects.all()
