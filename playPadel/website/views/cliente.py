from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import *


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
        num_campo = p.prenotazione.campo.numero
        dati_partita.append({
            'data': data,
            'ora': ora,
            'giocatori': lista_giocatori,
            'risultato': risultato,
            'nome_impianto': nome_impianto,
            'num_campo': num_campo
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
    dati_prenotazione = []
    for pren in prenotazione:
        pren_id = pren.id
        data = pren.data
        ora_inizio = pren.ora_inizio
        ora_fine = pren.ora_fine
        nome_impianto = pren.impianto.nome
        num_campo = pren.campo.numero
        if pren.data < today:
            stato = "Passato"
        elif pren.data >= today:
            stato = "Attivo"
        dati_prenotazione.append({
            'pren_id': pren_id,
            'stato': stato,
            'data': data,
            'ora_inizio': ora_inizio,
            'ora_fine': ora_fine,
            'nome_impianto': nome_impianto,
            'num_campo': num_campo
        })
    context = {
        'user': user,
        'prenotazione': prenotazione,
        'dati_prenotazione': dati_prenotazione,
        'pre_url': pre_url,
        'dashboard_url': d_url
    }
    return render(request, 'cliente/prenotazioni_cliente.html', context)
