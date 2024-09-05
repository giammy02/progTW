from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory

from .models import *


# Form per username e password valido per entrambi i tipi di user
class UserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Users


# Seconda colonna del form per nome, cognome ed email (valido per entrambi gli user)
class Step2UserForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label="Nome")
    last_name = forms.CharField(required=True, label="Cognome")
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email']


# Form specifico per Cliente per impostare foto profilo
class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['foto']


# Form specifico per Gestore per impostare foto profilo
class GestoreForm(forms.ModelForm):

    class Meta:
        model = Gestore
        fields = ['foto']


# Form per la creazione di un nuovo impianto
class ImpiantoForm(forms.ModelForm):

    class Meta:
        model = Impianto
        fields = ['nome', 'foto', 'numero_campi', 'posizione', 'orari', 'prezzi', 'contatti', 'caratteristiche']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control-file'}),
            'numero_campi': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'posizione': forms.TextInput(attrs={'class': 'form-control'}),
            'orari': forms.TextInput(attrs={'class': 'form-control', 'label': 'Costo orario'}),
            'prezzi': forms.TextInput(attrs={'class': 'form-control'}),
            'contatti': forms.TextInput(attrs={'class': 'form-control'}),
            'caratteristiche': forms.TextInput(attrs={'class': 'form-control'})
        }


class CampoForm(forms.ModelForm):
    TIPI_CAMPO = [
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    ]

    tipologia = forms.ChoiceField(choices=TIPI_CAMPO, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Campo
        fields = ['numero', 'tipologia']

    def __init__(self, *args, **kwargs):
        super(CampoForm, self).__init__(*args, **kwargs)
        self.fields['numero'].widget.attrs['readonly'] = True

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
        fields = ['user', 'foto']
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control'}),
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
