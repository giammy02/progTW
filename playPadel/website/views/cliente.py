from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from ..forms import UserSignUpForm, Step2UserForm, ClienteForm, EditClienteForm, UserForm
from ..models import *


def registrazione_cliente(request):
    user_type = 'cliente'

    if request.method == 'POST':
        user_form = UserSignUpForm(request.POST)
        user_form2 = Step2UserForm(request.POST)
        cliente_form = ClienteForm(request.POST, request.FILES)

        if user_form.is_valid() and user_form2.is_valid() and cliente_form.is_valid():
            # Salva l'utente
            user = user_form.save(commit=False)
            user.is_cliente = True
            user.save()

            user.first_name = user_form2.cleaned_data['first_name']
            user.last_name = user_form2.cleaned_data['last_name']
            user.email = user_form2.cleaned_data['email']
            user.save()

            cliente = cliente_form.save(commit=False)
            cliente.user = user
            cliente.save()

            messages.success(request, 'Registrazione completata con successo!')
            return redirect('login')
        else:
            messages.error(request, 'Si è verificato un errore durante la fase di registrazione!')
    else:
        user_form = UserSignUpForm()
        user_form2 = Step2UserForm()
        cliente_form = ClienteForm()

    return render(request, 'registration/signup_form.html', {
        'user_type': user_type,
        'user_form': user_form,
        'user_form2': user_form2,
        'user_form3': cliente_form
    })


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


@login_required
def modificaCliente(request):
    utente = request.user
    pre_url = request.META.get('HTTP_REFERER')
    d_url = request.build_absolute_uri('/cliente/dashboard/')
    m_url = request.build_absolute_uri('/cliente/modifica/')

    if request.method == 'POST':
        cliente_form = EditClienteForm(request.POST, request.FILES, instance=request.user.cliente)
        user_form = UserForm(request.POST, instance=request.user)

        if cliente_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            cliente = cliente_form.save(commit=False)
            cliente.user = user
            cliente.save()

            # Gestione cambio password
            if cliente_form.cleaned_data['new_password1']:
                user.set_password(cliente_form.cleaned_data['new_password1'])
                user.save()
                update_session_auth_hash(request, user)  # Mantiene l'utente loggato dopo il cambio password

            messages.success(request, 'Profilo aggiornato correttamente')
            return redirect('website:cliente:dashboard_cliente')

        else:
            messages.error(request, 'Si è verificato un errore. Controlla i dati inseriti.')
    else:
        cliente_form = EditClienteForm(instance=request.user.cliente)
        user_form = UserForm(instance=request.user)

    context = {
        'user': utente,
        'pre_url': pre_url,
        'dashboard_url': d_url,
        'modifica_url': m_url,
        'cliente_form': cliente_form,
        'user_form': user_form
    }

    return render(request, 'cliente/modifica_cliente.html', context)
