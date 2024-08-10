from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from ..forms import GestoreSignUpForm
from ..models import Gestore


class GestoreSignUpView(CreateView):
    model = Gestore
    form_class = GestoreSignUpForm
    template_name = 'playPadel/signup_form.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('homepage.html')
