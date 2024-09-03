from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import CreateView

from ..forms import GestoreSignUpForm
from ..models import *


class GestoreSignUpView(CreateView):
    model = Gestore
    form_class = GestoreSignUpForm
    template_name = 'registration/signup_form.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('homepage.html')


@login_required
def dashboardGestore(request):
    user = request.user
    impianto = Impianto.objects.filter(gestore_id=user.pk).first()

    context = {
        'user': user,
        'impianto': impianto,
    }
    return render(request, 'gestore/dashboard_gestore.html', context)


def modificaGestore(request):
    user = request.user
    pre_url = request.META.get('HTTP_REFERER')
    d_url = request.build_absolute_uri('/cliente/dashboard/')
    context = {
        'user': user,
        'pre_url': pre_url,
        'dashboard_url': d_url
    }
    return render(request, 'gestore/modifica_gestore.html', context)


def modificaImpianto(request):
    user = request.user
    pre_url = request.META.get('HTTP_REFERER')
    d_url = request.build_absolute_uri('/cliente/dashboard/')
    context = {
        'user': user,
        'pre_url': pre_url,
        'dashboard_url': d_url
    }
    return render(request, 'gestore/modifica_impianto.html', context)