from django.urls import path, include
from .views import website, cliente, gestore

app_name = 'website'

urlpatterns = [
    path('', website.homepage, name='homepage'),
    path('prenota/', website.prenota, name='prenota'),

    path('impianti/', include(([
        path('', website.ImpiantiList.as_view(), name='impianti'),
        path('cerca_impianto/', website.CercaImpiantoList.as_view(), name='cerca_impianto'),
        path('<slug:slug>/', website.ImpiantoDetail.as_view(), name='impianto_detail'),
        path('<slug:slug>/conferma_prenotazione/', website.conferma_prenotazione, name='conferma_prenotazione'),
    ], 'website'), namespace='website')),

    path('cliente/', include(([
        path('registrati/', cliente.ClienteSignUpView.as_view(), name='registra_cliente'),
        path('dashboard/', cliente.dashboardCliente, name='dashboard_cliente'),
    ], 'website'), namespace='cliente')),

    path('gestore/', include(([
        path('registrati/', gestore.GestoreSignUpView.as_view(), name='registra_gestore'),
        path('dashboard/', gestore.dashboardGestore, name='dashboard_gestore'),
    ], 'website'), namespace='gestore')),
]
