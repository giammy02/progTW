"""
URL configuration for playPadel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from website.views import website, cliente, gestore

urlpatterns = [
    path('', include('website.urls')),
    path('accounts/login/', website.MyLoginView.as_view(), name='login'),
    path('accounts/logout/', website.logout_request, name='logout'),
    path('accounts/signup/', website.SignUpView.as_view(), name='registrati'),
    path('accounts/signup/cliente/', cliente.ClienteSignUpView.as_view(), name='registra_cliente'),
    path('accounts/signup/gestore/', gestore.GestoreSignUpView.as_view(), name='registra_gestore'),
    path('admin/', admin.site.urls),
]