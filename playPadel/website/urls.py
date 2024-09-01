from django.urls import path, include
from .views import website as website
from .views import cliente as cliente
from .views import gestore as gestore

app_name = 'website'

urlpatterns = [
    path('', website.homepage, name='homepage'),
    path('prenota/', website.Prenota.as_view(), name='prenota'),

    path('impianti/', include(([
        path('', website.ImpiantiList.as_view(), name='impianti'),
        path('cerca_impianto/', website.CercaImpiantoList.as_view(), name='cerca_impianto'),
        path('<slug:slug>/', website.ImpiantoDetail.as_view(), name='impianto_detail'),
        path('<slug:slug>/conferma_prenotazione/', website.conferma_prenotazione, name='conferma_prenotazione'),
    ], 'website'), namespace='website')),

    path('cliente/', include(([
        path('registrati/', cliente.ClienteSignUpView.as_view(), name='registra_cliente'),
        path('dashboard/', cliente.dashboardCliente, name='dashboard_cliente'),
        path('prenotazioni/', cliente.prenotazioniCliente, name='prenotazioni_cliente'),
        # path('storico/', cliente.storicoCliente, name='storico_cliente'),
        path('modifica/', cliente.modificaCliente, name='modifica_cliente'),
    ], 'cliente'), namespace='cliente')),

    path('gestore/', include(([
        path('registrati/', gestore.GestoreSignUpView.as_view(), name='registra_gestore'),
        path('dashboard/', gestore.dashboardGestore, name='dashboard_gestore'),
    ], 'gestore'), namespace='gestore')),
]
