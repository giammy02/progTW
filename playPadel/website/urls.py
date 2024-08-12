from django.urls import path
from .views import website, cliente, gestore

app_name = 'website'

urlpatterns = [
    path('', website.homepage, name='homepage'),
    path('impianti/', website.ImpiantiList.as_view(), name='impianti'),
    path('impianti/<slug:slug>/', website.ImpiantoDetail.as_view(), name='impianto_detail'),
    # path('impianti/<slug:slug>/prenota/', website.prenota, name='prenotazione'),
    path('prenota/', website.prenota, name='prenota')
]
