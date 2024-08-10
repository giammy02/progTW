from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView

from ..models import Impianto


class SignUpView(TemplateView):
    template_name = 'PlayPadel/register.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('gestore:quiz_change_list')  # PAGINA MODIFICA IMPIANTI
        else:
            return redirect('cliente:quiz_list')  # PAGINA LISTA IMPIANTI
    return render(request, 'website/homepage.html')


class ImpiantiDetails(DetailView):
    model = Impianto
    template_name = 'website/impianti.html'


def prenota(request):
    return render(request, 'website/prenota.html')
