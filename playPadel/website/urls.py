from django.urls import path
from .views import website, cliente, gestore

app_name = 'website'

urlpatterns = [
    path('', website.homepage, name='homepage'),
    path('impianti/', website.ImpiantiList.as_view(), name='impianti'),
    path('impianti/cerca_impianto/', website.CercaImpiantoList.as_view(), name='cerca_impianto'),
    path('impianti/<slug:slug>/', website.ImpiantoDetail.as_view(), name='impianto_detail'),
    path('prenota/', website.prenota, name='prenota'),
    path('conferma_prenotazione/', website.conferma_prenotazione, name='conferma_prenotazione'),
]
