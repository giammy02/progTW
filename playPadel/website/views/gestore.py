from datetime import datetime

from django.contrib import messages
from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.defaultfilters import slugify

from ..forms import ImpiantoForm, CampoForm, NewsForm
from ..models import *


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
                form.fields['numero'].initial = idx
                form.fields['numero'].widget.attrs['readonly'] = True

            impianto_form = ImpiantoForm(instance=impianto)
            for field in impianto_form.fields.values():
                field.widget.attrs['disabled'] = True
        else:
            # Fase 1: Visualizzazione del form per l'impianto
            impianto_form = ImpiantoForm()
            campo_formset = None

    return render(request, 'gestore/crea_impianto.html', {
        'impianto_form': impianto_form,
        'campo_formset': campo_formset,
    })


@login_required
def crea_news(request):
    user = request.user
    impianto = Impianto.objects.filter(gestore_id=user.pk).first()

    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.gestore = user
            news.impianto = impianto
            news.data = timezone.now()
            news.save()

            messages.success(request, 'Notizia creata con successo!')
        else:
            messages.error(request, 'Errore nella creazione della notizia!')

    return redirect('website:gestore:dashboard_gestore')


@login_required
def dashboardGestore(request):
    user = request.user

    impianto = Impianto.objects.filter(gestore_id=user.pk).first()
    if not impianto:
        messages.error(request, 'Non hai ancora creato un impianto!')
        return redirect('website:gestore:crea_impianto_gestore')
    news_list = News.objects.filter(gestore_id=user.pk)
    prenotazione = Prenotazione.objects.filter(impianto_id=impianto.pk)

    today = datetime.now().date()
    prenotazioni_clienti = []
    for p in prenotazione:
        if p.data >= today:
            prenotazioni_clienti.append(p)

    news_forms = {news.pk: NewsForm(instance=news) for news in news_list}

    context = {
        'user': user,
        'impianto': impianto,
        'news_list': news_list,
        'prenotazioni_clienti': prenotazioni_clienti,
        'modifica_news_form': news_forms
    }
    return render(request, 'gestore/dashboard_gestore.html', context)


# View per la modifica di una news, usa lo stesso template della dashboard ma utilizza un form per la modifica
@login_required
def modifica_news(request, pk):
    article = get_object_or_404(News, id=pk, gestore=request.user)

    if request.method == 'POST':
        mod_news = NewsForm(request.POST, instance=article)
        if mod_news.is_valid():
            mod_news.save()
            messages.success(request, 'Notizia modificata con successo!')
        else:
            messages.error(request, 'Errore nella modifica della notizia.')

    return redirect('website:gestore:dashboard_gestore')


@login_required
def modificaImpianto(request, slug):
    user = request.user
    pre_url = request.META.get('HTTP_REFERER')
    d_url = request.build_absolute_uri('/gestore/dashboard/')
    m_url = request.build_absolute_uri('/gestore/modifica_impianto/')

    impianto = get_object_or_404(Impianto, slug=slug)
    campi = Campo.objects.filter(impianto=impianto)
    CampoFormSet = modelformset_factory(Campo, form=CampoForm, extra=0, can_delete=True)

    if request.method == 'POST':
        impianto_form = ImpiantoForm(request.POST, request.FILES, instance=impianto)
        numero_campi_nuovo = int(request.POST.get('numero_campi'))
        campo_formset = CampoFormSet(request.POST, queryset=campi)

        if impianto_form.is_valid() and campo_formset.is_valid():
            impianto = impianto_form.save(commit=False)

            # Se il numero di campi è cambiato
            numero_campi_corrente = campi.count()
            if numero_campi_nuovo > numero_campi_corrente:
                for i in range(numero_campi_corrente + 1, numero_campi_nuovo + 1):
                    Campo.objects.create(impianto=impianto, numero=i, tipologia='Indoor')

            impianto.save()
            campo_formset.save()
            messages.success(request, 'Impianto modificato con successo!')
            return redirect('website:gestore:dashboard_gestore')
    else:
        impianto_form = ImpiantoForm(instance=impianto)
        campo_formset = CampoFormSet(queryset=campi)

    context = {
        'user': user,
        'pre_url': pre_url,
        'dashboard_url': d_url,
        'm_impianto_url': m_url,
        'impianto_form': impianto_form,
        'campo_formset': campo_formset,
    }
    return render(request, 'gestore/modifica_impianto.html', context)

@login_required
def prenotazioniGestore(request):
    user = request.user
    pre_url = request.META.get('HTTP_REFERER')
    d_url = request.build_absolute_uri('/gestore/dashboard/')
    p_url = request.build_absolute_uri('/gestore/prenotazioni/')
    impianto = Impianto.objects.filter(gestore_id=user.pk).first()
    prenotazione = Prenotazione.objects.filter(impianto_id=impianto.pk)
    today = datetime.now().date()
    prenotazioni_clienti = []
    for p in prenotazione:
        if p.data >= today:
            prenotazioni_clienti.append(p)

    context = {
        'user': user,
        'pre_url': pre_url,
        'dashboard_url': d_url,
        'prenotazioni_url': p_url,
        'impianto': impianto,
        'prenotazioni_clienti': prenotazioni_clienti
    }
    return render(request, 'gestore/prenotazioni_clienti.html', context)