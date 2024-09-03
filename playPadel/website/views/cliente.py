from datetime import datetime

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
    partita = Partita.objects.filter(cliente_id=user.pk)
    dati_partita = []
    for p in partita:
        data = p.prenotazione.data
        ora = p.prenotazione.ora_inizio
        lista_giocatori = p.giocatori.split(', ')
        risultato = p.risultato.split(', ')
        nome_impianto = p.prenotazione.impianto.nome
        id_campo = p.prenotazione.campo_id
        dati_partita.append({
            'data': data,
            'ora': ora,
            'giocatori': lista_giocatori,
            'risultato': risultato,
            'nome_impianto': nome_impianto,
            'id_campo': id_campo
        })
    context = {
        'user': user,
        'prenotazioni': prenotazione,
        'dati_partita': dati_partita
    }
    return render(request, 'cliente/dashboard_cliente.html', context)


@login_required
def prenotazioniCliente(request):
    user = request.user
    prenotazione = Prenotazione.objects.filter(cliente_id=user.pk)
    pre_url = request.META.get('HTTP_REFERER')
    d_url = request.build_absolute_uri('/cliente/dashboard/')
    today = datetime.now().date()
    now = datetime.now().time()
    dati_prenotazione = []
    for pren in prenotazione:
        pren_id = pren.id
        data = pren.data
        ora_inizio = pren.ora_inizio
        ora_fine = pren.ora_fine
        nome_impianto = pren.impianto.nome
        id_campo = pren.campo_id
        if pren.data < today:
            stato = "Passato"
        elif pren.data >= today and pren.ora_inizio >= now:
            stato = "Attivo"
        dati_prenotazione.append({
            'pren_id': pren_id,
            'stato': stato,
            'data': data,
            'ora_inizio': ora_inizio,
            'ora_fine': ora_fine,
            'nome_impianto': nome_impianto,
            'id_campo': id_campo,
        })
    context = {
        'user': user,
        'prenotazione': prenotazione,
        'dati_prenotazione': dati_prenotazione,
        'pre_url': pre_url,
        'dashboard_url': d_url
    }
    return render(request, 'cliente/prenotazioni_cliente.html', context)


@login_required
def modificaCliente(request):
    user = request.user
    pre_url = request.META.get('HTTP_REFERER')
    d_url = request.build_absolute_uri('/cliente/dashboard/')
    context = {
        'user': user,
        'pre_url': pre_url,
        'dashboard_url': d_url
    }
    return render(request, 'cliente/modifica_cliente.html', context)
