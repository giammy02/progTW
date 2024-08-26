from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic import DetailView, TemplateView

from ..models import *
from ..forms import PrenotazioneForm


class SignInView(TemplateView):
    template_name = 'playPadel/login.html'


class SignUpView(TemplateView):
    template_name = 'playPadel/signup.html'


def homepage(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            pass
            # return redirect('website:impianti')  # PAGINA MODIFICA IMPIANTI
        else:
            pass
            # return redirect('website:impianti')  # PAGINA LISTA IMPIANTI
    return render(request, 'website/homepage.html')


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

    def post(self, request, *args, **kwargs):
        form = PrenotazioneForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., save the booking)
            return redirect('website:conferma_prenotazione')
        else:
            return self.render_to_response(self.get_context_data(form=form))


def prenota(request):
    return render(request, 'website/prenota.html')


def conferma_prenotazione(request):
    return render(request, 'website/conferma_prenotazione.html')
