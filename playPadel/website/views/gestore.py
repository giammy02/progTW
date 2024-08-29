from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import CreateView

from ..forms import GestoreSignUpForm
from ..models import Gestore, Impianto, News


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
    # model = Impianto, News
    context = {
        'user': user,
        # filtrare Impianto e news
    }
    return render(request, 'gestore/dashboard_gestore.html', context)
