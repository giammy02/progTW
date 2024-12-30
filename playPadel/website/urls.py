from django.conf import settings
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf.urls import handler404, handler500

from .views import website as website
from .views import cliente as cliente
from .views import gestore as gestore

app_name = 'website'

urlpatterns = [
    path('', website.homepage, name='homepage'),
    path('cancella_prenotazione/<int:pk>/', website.delete_prenotazione),
    path('cancella_news/<int:pk>/', website.delete_news),


    path('impianti/', include(([
        path('', website.ImpiantiList.as_view(), name='impianti'),
        path('cerca_impianto/', website.CercaImpiantoList.as_view(), name='cerca_impianto'),
        path('<slug:slug>/', website.ImpiantoDetail.as_view(), name='impianto_detail'),
        path('<slug:slug>/get_prenotazioni/', website.get_prenotazioni, name='get_prenotazioni'),
        path('<slug:slug>/conferma_prenotazione/', website.conferma_prenotazione, name='conferma_prenotazione'),
    ], 'website'), namespace='website')),

    path('cliente/', include(([
        path('dashboard/', cliente.dashboardCliente, name='dashboard_cliente'),
        path('prenotazioni/', cliente.prenotazioniCliente, name='prenotazioni_cliente'),
        path('modifica/', website.modificaUser, name='modifica_cliente'),
        path('modifica_partita/<int:pk>/', cliente.modifica_partita, name='modifica_partita'),
    ], 'cliente'), namespace='cliente')),

    path('gestore/', include(([
        path('dashboard/', gestore.dashboardGestore, name='dashboard_gestore'),
        path('modifica/', website.modificaUser, name='modifica_gestore'),
        path('registra_impianto/', gestore.crea_impianto, name='crea_impianto_gestore'),
        path('modifica_impianto/<slug:slug>', gestore.modificaImpianto, name='modifica_impianto_gestore'),
        path('prenotazioni/', gestore.prenotazioniGestore, name='prenotazioni_gestore'),
        path('modifica_news/<int:pk>/', gestore.modifica_news, name='modifica_news'),
        path('crea_news/', gestore.crea_news, name='crea_news'),
    ], 'gestore'), namespace='gestore')),
]

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]

    handler404 = 'website.views.website.error_404'
    handler500 = 'website.views.website.error_500'
