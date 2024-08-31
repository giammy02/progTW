from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import CreateView, ListView

from ..forms import ClienteSignUpForm
from ..models import *


class ClienteSignUpView(CreateView):
    model = Cliente
    form_class = ClienteSignUpForm
    template_name = 'registration/signup_form.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('homepage.html')


def logout_request(request):
    logout(request)
    messages.success(request, 'Logout eseguito con successo!')
    return redirect("website:homepage")


@login_required
def dashboardCliente(request):
    user = request.user
    prenotazione = Prenotazione.objects.filter(cliente_id=user.pk)
    impianto = Impianto.objects.filter(id=prenotazione.values('impianto_id').first()['impianto_id'])
    campo = Campo.objects.filter(id=prenotazione.values('campo_id').first()['campo_id'])
    partita = Partita.objects.filter(cliente_id=user.pk)
    context = {
        'user': user,
        'prenotazioni': prenotazione,
        'impianto': impianto,
        'campo': campo,
        'partite': partita
    }
    return render(request, 'cliente/dashboard_cliente.html', context)


@login_required
def prenotazioniCliente(request):
    user = request.user
    prenotazione = Prenotazione.objects.filter(cliente_id=user.pk)
    context = {
        'user': user,
        'prenotazioni': prenotazione
    }
    return render(request, 'cliente/prenotazioni_cliente.html', context)


def storicoCliente(request):
    user = request.user
    prenotazione = Prenotazione.objects.filter(cliente_id=user.pk)
    impianto = Impianto.objects.filter(id=prenotazione.values('impianto_id').first()['impianto_id'])
    campo = Campo.objects.filter(id=prenotazione.values('campo_id').first()['campo_id'])
    partita = Partita.objects.filter(cliente_id=user.pk)
    context = {
        'user': user,
        'prenotazioni': prenotazione,
        'impianto': impianto,
        'campo': campo,
        'partite': partita
    }
    return render(request, 'cliente/storico_cliente.html', context)
