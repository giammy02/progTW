from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import CreateView

from ..forms import ClienteSignUpForm
from ..models import Cliente, Prenotazione, Partita


class ClienteSignUpView(CreateView):
    model = Cliente
    form_class = ClienteSignUpForm
    template_name = 'registration/signup_form.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('homepage.html')


def logout_request(request):
    logout(request)
    messages.success(request, 'Logout eseguito con successo!')
    return redirect("website:homepage")


@login_required
def dashboardCliente(request):
    user = request.user
    # model = Prenotazione, Partita
    context = {
        'user': user,
        # filtrare prenotazione e partita
    }
    return render(request, 'cliente/dashboard_cliente.html', context)

