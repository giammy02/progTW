from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from ..forms import ClienteSignUpForm
from ..models import Cliente


class ClienteSignUpView(CreateView):
    model = Cliente
    form_class = ClienteSignUpForm
    template_name = 'playPadel/signup_form.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('homepage.html')
