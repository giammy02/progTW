from django.urls import path, include
from .views import website as website
from .views import cliente as cliente
from .views import gestore as gestore

app_name = 'website'

urlpatterns = [
    path('', website.homepage, name='homepage'),
    path('prenota/', website.Prenota.as_view(), name='prenota'),
    path('cancella_prenotazione/<pk>/', website.delete_prenotazione),

    path('impianti/', include(([
        path('', website.ImpiantiList.as_view(), name='impianti'),
        path('cerca_impianto/', website.CercaImpiantoList.as_view(), name='cerca_impianto'),
        path('<slug:slug>/', website.ImpiantoDetail.as_view(), name='impianto_detail'),
        path('<slug:slug>/conferma_prenotazione/', website.conferma_prenotazione, name='conferma_prenotazione'),
    ], 'website'), namespace='website')),

    path('cliente/', include(([
        path('dashboard/', cliente.dashboardCliente, name='dashboard_cliente'),
        path('prenotazioni/', cliente.prenotazioniCliente, name='prenotazioni_cliente'),
        path('modifica/', website.modificaUser, name='modifica_cliente'),
    ], 'cliente'), namespace='cliente')),

    path('gestore/', include(([
        path('dashboard/', gestore.dashboardGestore, name='dashboard_gestore'),
        path('modifica/', website.modificaUser, name='modifica_gestore'),
        path('registra_impianto/', gestore.crea_impianto, name='crea_impianto_gestore'),
        path('modifica_impianto/<slug:slug>', gestore.modificaImpianto, name='modifica_impianto_gestore'),
        path('prenotazioni/', gestore.prenotazioniGestore, name='prenotazioni_gestore'),
    ], 'gestore'), namespace='gestore')),
]
