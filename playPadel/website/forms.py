from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


# Form per username e password
class UserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Users


# Seconda colonna del form per nome, cognome ed email
class Step2UserForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label="Nome")
    last_name = forms.CharField(required=True, label="Cognome")
    email = forms.EmailField(required=True, label="Email")
    foto = forms.FileInput(attrs={'class': 'form-control-file'})

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'foto']


# Form per la creazione di un nuovo impianto
class ImpiantoForm(forms.ModelForm):

    class Meta:
        model = Impianto
        fields = ['nome', 'posizione', 'orari', 'prezzi', 'contatti', 'caratteristiche', 'numero_campi', 'foto']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'posizione': forms.TextInput(attrs={'class': 'form-control'}),
            'orari': forms.TextInput(attrs={'class': 'form-control', 'label': 'Costo orario'}),
            'prezzi': forms.TextInput(attrs={'class': 'form-control'}),
            'contatti': forms.TextInput(attrs={'class': 'form-control'}),
            'caratteristiche': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_campi': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'foto': forms.FileInput(attrs={'class': 'form-control-file'}),
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


class EditUserForm(forms.ModelForm):
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
        model = Users
        fields = ['username', 'first_name', 'last_name', 'email', 'foto']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
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

    # Salvataggio immagine di default se form 'foto' viene svuotato per prevenire campo vuoto nel DB
    def save(self, commit=True):
        instance = super(EditUserForm, self).save(commit=False)

        if not self.cleaned_data['foto']:
            instance.foto = 'profile_pics/default_profile_pic.png'

        if commit:
            instance.save()

        return instance


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
