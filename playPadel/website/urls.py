from django.urls import path
from .views import website, cliente, gestore

app_name = 'website'

urlpatterns = [
    path('', website.homepage, name='homepage'),
    path('impianti/', website.ImpiantiList.as_view(), name='impianti'),
    path('impianti/<str:nome>', website.ImpiantoDetail.as_view(), name='impianto_detail'),
    path('prenota/', website.prenota, name='prenota')
]
