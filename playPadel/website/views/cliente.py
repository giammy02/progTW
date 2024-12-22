from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from ..models import *

from ..forms import PartitaForm


@login_required
def dashboardCliente(request):
    user = request.user
    prenotazione = Prenotazione.objects.filter(cliente_id=user.pk)
    partita_list = Partita.objects.filter(cliente_id=user.pk)
    dati_partita = []
    for p in partita_list:
        id = p.id
        data = p.prenotazione.data
        ora = p.prenotazione.ora_inizio
        lista_giocatori = p.giocatori.split(', ')
        risultato = p.risultato.split(', ')
        nome_impianto = p.prenotazione.impianto.nome
        num_campo = p.prenotazione.campo.numero
        dati_partita.append({
            'id': id,
            'data': data,
            'ora': ora,
            'giocatori': lista_giocatori,
            'risultato': risultato,
            'nome_impianto': nome_impianto,
            'num_campo': num_campo
        })

    partita_form = {partita.pk: PartitaForm(instance=partita) for partita in partita_list}

    context = {
        'user': user,
        'prenotazioni': prenotazione,
        'dati_partita': dati_partita,
        'form_mod_partita': partita_form
    }
    return render(request, 'cliente/dashboard_cliente.html', context)


@login_required
def modifica_partita(request, pk):
    partita = get_object_or_404(Partita, id=pk, cliente_id=request.user.pk)

    if request.method == 'POST':
        form = PartitaForm(request.POST, instance=partita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Partita modificata con successo!')
        else:
            messages.error(request, 'Errore nella modifica della partita.')

    return redirect('website:cliente:dashboard_cliente')


@login_required
def prenotazioniCliente(request):
    user = request.user
    prenotazione = Prenotazione.objects.filter(cliente_id=user.pk)
    pre_url = request.META.get('HTTP_REFERER')
    d_url = request.build_absolute_uri('/cliente/dashboard/')
    p_url = request.build_absolute_uri('/cliente/prenotazioni/')
    today = datetime.now().date()
    dati_prenotazione = []
    for pren in prenotazione:
        pren_id = pren.id
        data = pren.data
        ora_inizio = pren.ora_inizio
        ora_fine = pren.ora_fine
        nome_impianto = pren.impianto.nome
        num_campo = pren.campo.numero
        if pren.data <= today:
            stato = "Passato"
        elif pren.data > today:
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
        'dashboard_url': d_url,
        'prenotazioni_url': p_url
    }
    return render(request, 'cliente/prenotazioni_cliente.html', context)
