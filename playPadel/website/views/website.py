from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic import DetailView, TemplateView

from ..models import Impianto


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


def prenota(request):
    return render(request, 'website/prenota.html')
