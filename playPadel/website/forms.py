from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class ClienteSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Users

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_cliente = True
        if commit:
            user.save()
        return user


class GestoreSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Users

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user


class EditClienteForm(forms.ModelForm):
    old_password = forms.CharField(
        label="Vecchia Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={"required": "Inserire la vecchia password per validare le modifiche"}
    )
    new_password1 = forms.CharField(
        label="Nuova Password",
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label="Conferma Nuova Password",
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Cliente
        fields = ['user', 'eta', 'foto']
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control'}),
            'eta': forms.NumberInput(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    # Validazione personalizzata per le password
    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        # Verifica che la nuova password sia inserita correttamente
        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('new_password2', "Le nuove password non corrispondono.")

        return cleaned_data


class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class PrenotazioneForm(forms.ModelForm):

    class Meta:
        model = Prenotazione
        fields = ['data']
        widgets = {'data': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }


class CercaDisponibilita(forms.ModelForm):

    class Meta:
        model = Prenotazione
        fields = ['data']
        widgets = {'data': forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'date',
        }),
        }
