from datetime import datetime

from django.contrib import messages
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.defaultfilters import slugify

from ..forms import UserSignUpForm, Step2UserForm, GestoreForm, ImpiantoForm, CampoForm
from ..models import *


def registrazione_gestore(request):
    user_type = 'gestore'

    if request.method == 'POST':
        user_form = UserSignUpForm(request.POST)
        user_form2 = Step2UserForm(request.POST)
        gestore_form = GestoreForm(request.POST, request.FILES)

        if user_form.is_valid() and user_form2.is_valid() and gestore_form.is_valid():
            # Salva l'utente
            user = user_form.save(commit=False)
            user.is_staff = True
            user.save()

            user.first_name = user_form2.cleaned_data['first_name']
            user.last_name = user_form2.cleaned_data['last_name']
            user.email = user_form2.cleaned_data['email']
            user.save()

            gestore = gestore_form.save(commit=False)
            gestore.user = user
            gestore.save()

            messages.info(request, "Registrazione avvenuta! Proseguire con il login per creare l'impianto")
            return redirect('website:gestore:crea_impianto_gestore')
        else:
            messages.error(request, 'Si è verificato un errore durante la fase di registrazione!')
    else:
        user_form = UserSignUpForm()
        user_form2 = Step2UserForm()
        gestore_form = GestoreForm()

    return render(request, 'registration/signup_form.html', {
        'user_type': user_type,
        'user_form': user_form,
        'user_form2': user_form2,
        'user_form3': gestore_form
    })

@login_required
def crea_impianto(request):
    if request.method == 'POST':
        if 'impianto_id' in request.session:
            # Fase 2: Impianto già creato procedo con la creazione dei campi
            impianto_id = request.session['impianto_id']
            impianto = Impianto.objects.get(id=impianto_id)

            numero_campi = impianto.numero_campi
            CampoFormSet = inlineformset_factory(
                Impianto, Campo, form=CampoForm, extra=numero_campi, can_delete=False
            )
            campo_formset = CampoFormSet(request.POST, instance=impianto)

            if campo_formset.is_valid():
                campi = campo_formset.save(commit=False)
                for idx, campo in enumerate(campi, start=1):
                    campo.numero = idx  # Imposta il numero progressivo del campo
                    campo.save()

                del request.session['impianto_id']
                messages.success(request, 'Impianto creato con successo!')
                return redirect('website:homepage')

        else:
            # Fase 1: Creazione impianto
            impianto_form = ImpiantoForm(request.POST, request.FILES)

            if impianto_form.is_valid():
                impianto = impianto_form.save(commit=False)
                impianto.gestore_id = request.user.pk
                impianto.slug = slugify(impianto.nome)
                impianto.save()

                request.session['impianto_id'] = impianto.id

                return redirect('website:gestore:crea_impianto_gestore')

    else:
        if 'impianto_id' in request.session:
            # Fase 2: Visualizzazione del formset per i campi
            impianto_id = request.session['impianto_id']
            impianto = Impianto.objects.get(id=impianto_id)

            # Numero di campi basato sul form dell'impianto
            numero_campi = impianto.numero_campi
            CampoFormSet = inlineformset_factory(Impianto, Campo, form=CampoForm, extra=numero_campi, can_delete=False)
            campo_formset = CampoFormSet(instance=impianto)

            for idx, form in enumerate(campo_formset.forms, start=1):
                form.fields['numero'].initial = idx  # Imposta il numero progressivo
                form.fields['numero'].widget.attrs['readonly'] = True  # Rendi il campo non modificabile

            impianto_form = ImpiantoForm(instance=impianto)
            for field in impianto_form.fields.values():
                field.widget.attrs['disabled'] = True
        else:
            # Fase 1: Visualizzazione del form per l'impianto
            impianto_form = ImpiantoForm()
            campo_formset = None  # Il formset non è ancora necessario

    return render(request, 'gestore/crea_impianto.html', {
        'impianto_form': impianto_form,
        'campo_formset': campo_formset,
    })


@login_required
def dashboardGestore(request):
    user = request.user
    impianto = Impianto.objects.filter(gestore_id=user.pk).first()
    news = News.objects.filter(impianto_id=impianto.pk)
    prenotazione = Prenotazione.objects.filter(impianto_id=impianto.pk)
    today = datetime.now().date()
    prenotazioni_clienti = []
    for p in prenotazione:
        if p.data >= today:
            prenotazioni_clienti.append(p)
    context = {
        'user': user,
        'impianto': impianto,
        'news': news,
        'prenotazioni_clienti': prenotazioni_clienti
    }
    return render(request, 'gestore/dashboard_gestore.html', context)


def modificaGestore(request):
    user = request.user
    pre_url = request.META.get('HTTP_REFERER')
    d_url = request.build_absolute_uri('/gestore/dashboard/')
    m_url = request.build_absolute_uri('/gestore/modifica/')

    context = {
        'user': user,
        'pre_url': pre_url,
        'dashboard_url': d_url,
        'modifica_url': m_url
    }
    return render(request, 'gestore/modifica_gestore.html', context)


def modificaImpianto(request):
    user = request.user
    pre_url = request.META.get('HTTP_REFERER')
    d_url = request.build_absolute_uri('/gestore/dashboard/')
    m_url = request.build_absolute_uri('/gestore/modifica_impianto/')

    context = {
        'user': user,
        'pre_url': pre_url,
        'dashboard_url': d_url,
        'm_impianto_url': m_url
    }
    return render(request, 'gestore/modifica_impianto.html', context)
