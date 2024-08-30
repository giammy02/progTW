from datetime import datetime

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
