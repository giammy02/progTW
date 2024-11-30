from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic import DetailView, TemplateView
from django.db.models import Q

from ..models import *
from ..forms import PrenotazioneForm, UserSignUpForm, Step2UserForm, EditUserForm


def homepage(request):
    return render(request, 'website/homepage.html')


class MyLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Credenziali non valide. Riprova.')
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'Login eseguito con successo!')
        return super().form_valid(form)


def logout_request(request):
    logout(request)
    messages.success(request, 'Logout eseguito con successo!')
    return redirect("website:homepage")


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def registrazione_utente(request):
    if request.path == '/accounts/signup/gestore/':
        user_type = 'gestore'
    elif request.path == '/accounts/signup/cliente/':
        user_type = 'cliente'

    if request.method == 'POST':
        user_form = UserSignUpForm(request.POST)
        user_form2 = Step2UserForm(request.POST, request.FILES)

        if user_form.is_valid() and user_form2.is_valid():
            # Salva l'utente
            user = user_form.save(commit=False)
            if user_type == 'gestore':
                user.is_staff = True

            user.first_name = user_form2.cleaned_data['first_name']
            user.last_name = user_form2.cleaned_data['last_name']
            user.email = user_form2.cleaned_data['email']
            user.foto = user_form2.cleaned_data['foto']
            user.save()

            if user_type == 'gestore':
                messages.info(request, "Registrazione avvenuta! Proseguire con il login per creare l'impianto")
                return redirect('website:gestore:crea_impianto_gestore')
            else:
                messages.success(request, 'Registrazione completata con successo!')
                return redirect('login')
        else:
            messages.error(request, 'Si è verificato un errore durante la fase di registrazione!')
    else:
        user_form = UserSignUpForm()
        user_form2 = Step2UserForm()

    context = {
        'user_type': user_type,
        'user_form': user_form,
        'user_form2': user_form2
    }

    return render(request, 'registration/signup_form.html', context)


@login_required
def modificaUser(request):
    if request.user.is_staff:
        user_type = 'gestore'
    else:
        user_type = 'cliente'
    username = request.user.username
    pre_url = request.META.get('HTTP_REFERER')
    d_url = request.build_absolute_uri('/'+user_type+'/dashboard/')
    m_url = request.build_absolute_uri('/'+user_type+'cliente/modifica/')

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, request.FILES, instance=request.user)

        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if user_form.is_valid():
            # Verifica della vecchia password
            if old_password and authenticate(username=username, password=old_password):
                # Verifica se sono stati inseriti nuovi campi password
                if new_password1 and new_password2:
                    if new_password1 == new_password2:
                        user = user_form.save(commit=False)
                        if not user_form.cleaned_data['foto']:
                            user.foto = 'profile_pics/default_profile_pic.png'
                        user.set_password(new_password1)  # Imposta la nuova password
                        user.save()

                        update_session_auth_hash(request, user)  # Mantiene l'utente loggato dopo il cambio password
                        messages.success(request, 'Profilo e password aggiornati correttamente.')
                        return redirect('website:'+user_type+':dashboard_'+user_type)
                    else:
                        messages.error(request, 'Le nuove password non coincidono.')
                else:
                    # Salva i dati dell'utente senza cambiare la password
                    user = user_form.save(commit=False)
                    if not user_form.cleaned_data['foto']:
                        user.foto = 'profile_pics/default_profile_pic.png'
                    user.save()
                    messages.success(request, 'Profilo aggiornato correttamente.')
                    return redirect('website:'+user_type+':dashboard_'+user_type)
            else:
                messages.error(request, 'La vecchia password non è corretta.')
        else:
            messages.error(request, 'Si è verificato un errore. Controlla i dati inseriti.')
    else:
        user_form = EditUserForm(instance=request.user)

    context = {
        'user_type': user_type,
        'pre_url': pre_url,
        'dashboard_url': d_url,
        'modifica_url': m_url,
        'user_form': user_form
    }

    return render(request, 'website/modifica_user.html', context)


class ImpiantiList(ListView):
    model = Impianto
    template_name = 'website/impianti.html'


class ImpiantoDetail(DetailView):
    model = Impianto
    template_name = 'website/impianto_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Collegamento tra tabella campi e impianto
        context['campo'] = Campo.objects.filter(impianto_id=self.get_object().pk)

        # Collegamento con tabella news dell'impianto
        context['news'] = News.objects.filter(impianto_id=self.get_object().pk)

        # DatePicker
        context['form'] = PrenotazioneForm()

        # Formattazione campo orari
        orario = self.object.orari
        orario_inizio, orario_fine = orario.split(" - ")
        formato_orario = "%H:%M"
        inizio = datetime.strptime(orario_inizio, formato_orario)
        if orario_fine == "24:00":
            orario_fine = "00:00"
            fine = datetime.strptime(orario_fine, formato_orario) + timedelta(days=1)
        else:
            fine = datetime.strptime(orario_fine, formato_orario)
        differenza_orario = int((fine-inizio).total_seconds() / 3600)
        context['inizio'] = orario_inizio
        context['differenza_orario'] = range(0, differenza_orario)
        ore = []
        ora_corrente = inizio
        while ora_corrente < fine:
            ore.append(ora_corrente.strftime('%H:%M'))
            ora_corrente += timedelta(hours=1)
        context['ore'] = ore

        return context

    # Ottieni prenotazioni dell'impianto
    def get_prenotazioni(self, request, *args, **kwargs):
        campo_id = request.GET.get('campo_id')
        data = request.GET.get('data')

        if campo_id and data:
            campo = get_object_or_404(Campo, id=campo_id)
            prenotazioni = Prenotazione.objects.filter(campo=campo, data=data)
            orari_prenotati = []

            for prenotazione in prenotazioni:
                orari_prenotati.append({
                    'ora_inizio': prenotazione.ora_inizio.strftime('%H:%M'),
                    'ora_fine': prenotazione.ora_fine.strftime('%H:%M')
                })

            return JsonResponse({'orari_prenotati': orari_prenotati})

        return JsonResponse({'error': 'Dati non validi'}, status=400)

    # Effettua prenotazione
    @login_required
    def post(self, request, slug, *args, **kwargs):
        form = PrenotazioneForm(request.POST)
        if form.is_valid():
            return redirect('website:website:conferma_prenotazione', slug=slug)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class CercaImpiantoList(ListView):
    model = Impianto
    template_name = "website/cerca_impianto.html"

    def get_queryset(self):
        name = self.request.GET.get("name")  # Nome impianto
        pos = self.request.GET.get("pos")  # Posizione
        mnc = self.request.GET.get("mnc")  # Numero minimo campi
        pm = self.request.GET.get("pm")  # Prezzo massimo
        ind = self.request.GET.get("ind")  # Indoor
        out = self.request.GET.get("out")  # Outdoor
        ccNoleggio = self.request.GET.get("ccNoleggio")  # Caratteristiche: Noleggio
        ccSpogliatoi = self.request.GET.get("ccSpogliatoi")  # Caratteristiche: Spogliatoi
        ccDocce = self.request.GET.get("ccDocce")  # Caratteristiche: Docce
        ccBar = self.request.GET.get("ccBar")  # Caratteristiche: Bar
        ccParcheggio = self.request.GET.get("ccParcheggio")  # Caratteristiche: Parcheggio
        ccAltro = self.request.GET.get("ccAltro")  # Caratteristiche: Altro
        queries = []

        if name:
            queries.append(Q(nome__icontains=name))
        if pos:
            queries.append(Q(posizione__icontains=pos))
        if mnc:
            queries.append(Q(numero_campi__gte=mnc))
        if pm:
            queries.append(Q(prezzi__lte=pm))
        if ind == 'on':
            queries.append(Q(id__in=Campo.objects.filter(tipologia='Indoor').values_list('impianto', flat=True)))
        if out == 'on':
            queries.append(Q(id__in=Campo.objects.filter(tipologia='Outdoor').values_list('impianto', flat=True)))
        if ccNoleggio == 'on':
            queries.append(Q(caratteristiche__icontains="Noleggio"))
        if ccSpogliatoi == 'on':
            queries.append(Q(caratteristiche__icontains="Spogliatoi"))
        if ccDocce == 'on':
            queries.append(Q(caratteristiche__icontains="Docce"))
        if ccBar == 'on':
            queries.append(Q(caratteristiche__icontains="Bar"))
        if ccParcheggio == 'on':
            queries.append(Q(caratteristiche__icontains="Parcheggio"))
        if ccAltro == 'on':
            queries.append(Q(caratteristiche__icontains=""))

        if queries:
            object_list = Impianto.objects.filter(*queries)
        else:
            object_list = Impianto.objects.all()
        return object_list

class Prenota(ListView):
    model = Impianto
    template_name = "website/prenota.html"

    # Cercare impianti che hanno disponibilità e redirect a pagina impianto

    '''
    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Impianto.objects.filter(
            Q(nome__icontains=query) | Q(caratteristiche__icontains=query)
        )
        return object_list
    '''


@login_required
def conferma_prenotazione(request, slug):
    impianto = get_object_or_404(Impianto, slug=slug)
    return render(request, 'website/conferma_prenotazione.html', {
        'slug': slug,
        'impianto': impianto
    })


@login_required
def delete_prenotazione(request, pk):
    post = Prenotazione.objects.get(pk=pk)
    pre_url = request.META.get('HTTP_REFERER')
    post.delete()
    messages.success(request, "Prenotazione cancellata!")
    return redirect(pre_url)


@login_required
def delete_news(request, pk):
    post = News.objects.get(pk=pk)
    pre_url = request.META.get('HTTP_REFERER')
    post.delete()
    messages.success(request, "News cancellata!")
    return redirect(pre_url)
