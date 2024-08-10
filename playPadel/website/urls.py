from django.urls import path
from .views import website, cliente, gestore

app_name = 'website'

urlpatterns = [
    path('impianti/<str:nome>', website.ImpiantiDetails.as_view(), name='impianti_detail'),
    path('prenota/', website.prenota, name='prenota')
]
